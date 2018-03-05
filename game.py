from pygame.sprite import Group
from time import time
from bullet import Bullet
from effects import hit
from ship import Ship
from level import Level
import pygame


class Game():
    def __init__(self, s, gfx, int_screen, status):
        self.s = s
        self.gfx = gfx
        self.int_screen = int_screen
        self.status = status

        # Init level
        self.level = Level(self.s, self.gfx, self.int_screen, self.status.level)

        # Init ship and bullets
        self.ship = Ship(self.int_screen, self.s, self.gfx)
        self.bullets = Group()
        self.enemy_bullets = Group()
        self.effects = Group()

    def check_events(self):
        """Respond to keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self, event):
        """Respond to key press"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self.status.game_running = False

    def check_keyup_events(self, event):
        """Respond to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.ship.moving_center = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.ship.moving_center = True

    def fire_bullet(self):
        # Set shooting flag
        self.ship.shooting = True
        # Set shooting timer
        self.ship.shooting_timer = time() + 0.1
        # Add bullet
        if len(self.bullets) < self.s.bullet_count:
            self.bullets.add(Bullet(self.s, self.ship, self.gfx))

    def update_bullets(self, dt):
        """Manage bullets"""
        self.bullets.update(dt)
        self.enemy_bullets.update(dt)

        # Get rid of bullet out of screen
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets:
            if bullet.rect.top >= self.s.int_screen_height:
                self.enemy_bullets.remove(bullet)

    def check_collisions(self):
        # Check collisions between bullets and enemies, bullets get removed automatically
        dict = pygame.sprite.groupcollide(self.level.enemies, self.bullets, False, True, pygame.sprite.collide_mask)
        for enemy in dict.keys():
            # Create effects on impacting bullets
            for bullet in dict[enemy]:
                self.effects.add(hit.Hit([bullet.rect.centerx, bullet.rect.top], self.gfx))

            enemy.hit()
            if enemy.health <= 0:
                self.status.score += enemy.reward
                self.level.enemies.remove(enemy)

        # check collisions between player and enemy bullets
        dict = pygame.sprite.spritecollide(self.ship, self.enemy_bullets, True, pygame.sprite.collide_mask)
        for bullet in dict:
            self.status.lives -= 1

        # Check collisions between player and enemies
        list = pygame.sprite.spritecollide(self.ship, self.level.enemies, True, pygame.sprite.collide_mask)
        if list:
            self.status.lives -= 1

    def draw(self):
        """ Draw game objects to internal screen """
        # Draw level
        if self.level.draw():
            # Draw ship
            self.ship.blitme()

            # Draw bullets
            for bullet in self.bullets.sprites():
                bullet.blitme(self.int_screen)
            for bullet in self.enemy_bullets.sprites():
                bullet.blitme(self.int_screen)

            # Draw effects
            for effect in self.effects:
                effect.blitme(self.int_screen)

    def update(self, dt):
        if not self.status.dead:
            if self.level.update(dt, self.enemy_bullets, self.ship):
                self.check_events()
                self.ship.update(dt)
                self.bullets.update(dt)
                self.enemy_bullets.update(dt)
                self.check_collisions()
                self.effects.update(dt)
                if self.level.ending:
                    if self.level.next_level == '':
                        self.status.lives = 0
                    else:
                        self.status.level = self.level.next_level
                        return True

        return False
