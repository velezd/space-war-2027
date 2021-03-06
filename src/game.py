import pygame
from pygame.sprite import Group
from time import time
from bullet import Bullet
from effects import hit
from ship import Ship
from level import Level
from config import CFG
from sfx import SFX
from events import Events


class Game():
    def __init__(self, int_screen, status):
        self.int_screen = int_screen
        self.status = status

        # Init level
        self.level = Level(self.int_screen, self.status.level)

        # Init ship and bullets
        self.ship = Ship(self.int_screen)
        self.bullets = Group()
        self.enemy_bullets = Group()
        self.effects = Group()
        self.pickups = Group()

    def check_events(self):
        """Respond to keyboard and mouse events"""
        # Respond to key press
        if Events().right_pressed:
            self.ship.moving_right = True
        if Events().left_pressed:
            self.ship.moving_left = True
        if Events().fire1_pressed:
            self.fire_bullet()
        if Events().cancel_pressed:
            self.status.game_running = False
        # Respond to key release
        if Events().right_released:
            self.ship.moving_right = False
            self.ship.moving_center = True
        if Events().left_released:
            self.ship.moving_left = False
            self.ship.moving_center = True

    def fire_bullet(self):
        # Set shooting flag
        self.ship.shooting = True
        # Set shooting timer
        self.ship.shooting_timer = time() + 0.1
        # Add bullet
        if len(self.bullets) < CFG().bullet_count:
            self.bullets.add(Bullet(self.ship))
            SFX().blaster1.play()

    def update_bullets(self, dt):
        """Manage bullets"""
        self.bullets.update(dt)
        self.enemy_bullets.update(dt)

        # Get rid of bullet out of screen
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets:
            if bullet.rect.top >= CFG().int_screen_height:
                self.enemy_bullets.remove(bullet)

    def check_collisions(self):
        # Check collisions between bullets and enemies, bullets get removed automatically
        dict = pygame.sprite.groupcollide(self.level.enemies, self.bullets, False, True, pygame.sprite.collide_mask)
        for enemy in dict.keys():
            # Create effects on impacting bullets
            for bullet in dict[enemy]:
                self.effects.add(hit.Hit([bullet.rect.centerx, bullet.rect.top]))

            enemy.hit()
            if enemy.health <= 0:
                if enemy.pickup:
                    self.pickups.add(enemy.pickup([enemy.rect.centerx, enemy.rect.centery]))
                self.effects.add(hit.Explosion([enemy.rect.centerx, enemy.rect.centery]))
                self.status.score += enemy.reward
                self.level.enemies.remove(enemy)
                SFX().boom1.play()

        # check collisions between player and enemy bullets
        dict = pygame.sprite.spritecollide(self.ship, self.enemy_bullets, True, pygame.sprite.collide_mask)
        for bullet in dict:
            self.effects.add(hit.Hit([bullet.rect.centerx, bullet.rect.bottom]))
            self.ship.hit()
            self.status.lives -= 1
            SFX().boom1.play()

        # Check collisions between player and enemies
        list = pygame.sprite.spritecollide(self.ship, self.level.enemies, False, pygame.sprite.collide_mask)
        for enemy in list:
            self.effects.add(hit.Explosion([enemy.rect.centerx, enemy.rect.centery]))
            self.ship.hit()
            self.level.enemies.remove(enemy)
            self.status.lives -= 1
            SFX().boom1.play()

        # Check collisions between player and pickups
        list = pygame.sprite.spritecollide(self.ship, self.pickups, False)
        for pickup in list:
            pickup.pickup(self.status)

    def draw(self):
        """ Draw game objects to internal screen """
        # Draw level
        if self.level.draw():
            # Draw ship
            self.ship.blitme()
            # Draw pickups
            self.pickups.draw(self.int_screen)
            # Draw bullets
            self.bullets.draw(self.int_screen)
            self.enemy_bullets.draw(self.int_screen)
            # Draw effects
            self.effects.draw(self.int_screen)

    def update(self, dt):
        if not self.status.dead:
            if self.level.update(dt, self.enemy_bullets, self.ship, self.status):
                self.check_events()
                self.ship.update(dt)
                self.bullets.update(dt)
                self.enemy_bullets.update(dt)
                self.pickups.update(dt)
                self.check_collisions()
                self.effects.update(dt)
                if self.level.ending:
                    if self.level.next_level == '':
                        self.status.lives = 0
                    else:
                        self.status.level = self.level.next_level
                        return True

        return False
