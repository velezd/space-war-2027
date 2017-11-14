import pygame
from pygame import sprite
from sys import exit
from time import time
from bullet import Bullet


def check_events(s, ship, bullets, gfx, status):
    """Respond to keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, s, ship, bullets, gfx, status)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, s, ship, bullets, gfx, status):
    """Respond to key press"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(s, ship, bullets, gfx)
    elif event.key == pygame.K_ESCAPE:
        status.game_running = False


def check_keyup_events(event, ship):
    """Respond to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        ship.moving_center = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        ship.moving_center = True


def fire_bullet(s, ship, bullets, gfx):
    # Set shooting flag
    ship.shooting = True
    # Set shooting timer
    ship.shooting_timer = time() + 0.1
    # Add bullet
    if len(bullets) < s.bullet_count:
        bullets.add(Bullet(s, ship, gfx))


def update_bullets(bullets, enemy_bullets, s, dt):
    """Manage bullets"""
    bullets.update(dt)
    enemy_bullets.update(dt)

    # Get rid of bullet out of screen
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in enemy_bullets:
        if bullet.rect.top >= s.int_screen_height:
            enemy_bullets.remove(bullet)



def check_collisions(ship, enemies, bullets, enemy_bullets):
    # Check collisions between bullets and enemies, bullets get removed automatically
    dict = pygame.sprite.groupcollide(enemies, bullets, False, True, pygame.sprite.collide_mask)
    for enemy in dict.keys():
        enemy.hit()
        if enemy.health <= 0:
            enemies.remove(enemy)

    # check collisions between player and enemy bullets
    dict = pygame.sprite.spritecollide(ship, enemy_bullets, True, pygame.sprite.collide_mask)
    for bullet in dict:
        ship.killed()

    # Check collisions between player and enemies
    list = pygame.sprite.spritecollide(ship, enemies, True, pygame.sprite.collide_mask)
    if list:
        ship.killed()


def update_screen(s, screen, int_screen, text, clock, background, level, ship, bullets, enemy_bullets):
    """Update images on the screen and flip to the new screen."""
    screen.fill((25,25,25))

    # Draw background
    background.draw()

    level.draw()

    # Draw ship
    ship.blitme()

    # Draw bullets
    for bullet in bullets.sprites():
        bullet.blitme(int_screen)

    for bullet in enemy_bullets.sprites():
        bullet.blitme(int_screen)

    # Scale internal screen
    int_screen = pygame.transform.scale(int_screen, (s.int_scale_width, s.int_scale_height))

    # And put it on screen
    rect = int_screen.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(int_screen, rect)

    # Print fps
    text.write(str(int(clock.get_fps())), 5, 5)

    # Flip buffer
    pygame.display.flip()


def show_loading(screen, text):
    """Show loading screen, renders independently on rest of the game"""
    screen.fill((0,0,0))
    rect = screen.get_rect()
    text.write('now loading...', rect.centerx, rect.centery, (255,255,255), origin='center')
    pygame.display.flip()
