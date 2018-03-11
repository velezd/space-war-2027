import pygame
from sys import exit
from time import time
from gfx import Text
from pygame.sprite import Group, Sprite
from effects import stars
from highscores import HSEntry, HSDisplay
from config import CFG
from gfx import GFX


class Menu():
    def __init__(self, int_screen, status):
        self.int_screen = int_screen
        self.rect = self.int_screen.get_rect()
        self.status = status
        self.background = BackgroundImage(self.int_screen, GFX().menu_background['front'], [1,1])
        self.font = Text(self.int_screen, CFG().font_main, 16, (255, 255, 255))
        self.cursor = MenuLogo()

        self.hs_entry = HSEntry(int_screen, self.status)
        self.hs_display = HSDisplay(int_screen, self.status)

        self.stars = Group()
        stars.generate_init_stars(self.stars, 20, self.int_screen, 47)
        self.gen_speed = 0.1
        self.timer = 0
        self.menu_separation = 32

        self.menu_items = ['New Game', 'Continue', 'High Score', 'Exit']
        self.cursor_position = 0

    def draw(self):
        # Empty screen
        self.int_screen.fill((0, 0, 0))

        # Draw stars
        for star in self.stars.sprites():
            star.draw()

        # Draw background image
        self.background.draw(self.int_screen)

        if self.status.show_hs:
            if self.status.new_hs:
                self.hs_entry.draw()
            else:
                self.hs_display.draw()
        else:

            # Draw menu items
            for x in range(len(self.menu_items)):
                self.font.write(self.menu_items[x], self.rect.left + 64, self.rect.top + 100 + (x * self.menu_separation))

            # Draw cursor
            self.cursor.draw(self.int_screen)

    def update(self, game, dt):
        if self.status.show_hs:
            if self.status.new_hs:
                self.hs_entry.update()
            else:
                self.hs_display.update()
        else:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.cursor_position != 0:
                            self.cursor_position -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.cursor_position != len(self.menu_items)-1:
                            self.cursor_position += 1
                    elif event.key == pygame.K_RETURN:
                        self.evaluate(game)

            # Cursor animation and position
            self.cursor.rect.left = self.rect.left + 16
            self.cursor.rect.top = self.rect.top + 92 + self.cursor_position * self.menu_separation
            self.cursor.update()

        # Update stars
        self.stars.update(dt)
        # Add stars
        if self.timer < time():
            self.timer = time() + self.gen_speed
            self.stars.add(stars.Star(self.int_screen, 47))

    def evaluate(self, game):
        if self.cursor_position == 0:
            # New Game
            self.status.reset()
            game.__init__(self.int_screen, self.status)
            self.status.game_running = True
        elif self.cursor_position == 1:
            # Continue
            if self.status.dead:
                game.__init__(self.int_screen, self.status)
                self.status.dead = False
            self.status.game_running = True
        elif self.cursor_position == 2:
            # High Score
            self.status.show_hs = True
        elif self.cursor_position == 3:
            # Exit
            exit()


class BackgroundImage():
    """ Shows background image on the specified position with specified scale """
    def __init__(self, int_screen, image, place=[0,0], scale=1):
        screen_rect = int_screen.get_rect()

        self.image = image
        self.rect = self.image.get_rect()

        # Set background scale
        if scale != 1:
            self.image = pygame.transform.scale(self.image, (self.rect.width * scale, self.rect.height * scale))
            self.rect = self.image.get_rect()

        # Set background position
        if place[0] == 0:     # center
            self.rect.centerx = screen_rect.centerx
        elif place[0] == 1:   # right
            self.rect.right = screen_rect.right - 20
        else:                   # left
            self.rect.left = screen_rect.left + 20
        if place[1] == 0:     # center
            self.rect.centery = screen_rect.centery
        elif place[1] == 1:   # top
            self.rect.top = screen_rect.top + 20
        else:                   # bottom
            self.rect.bottom = screen_rect.bottom - 20

    def draw(self, surface):
        """Draw background image"""
        surface.blit(self.image, self.rect)


class MenuLogo(Sprite):
    """Spinning logo that marks menu selection"""
    def __init__(self):
        super(MenuLogo, self).__init__()
        self.image = GFX().logo
        self.rect = self.image.get_rect()
        self.size = self.rect.height

        self.timer = 0
        self.frame = 0

        self.num_frames = self.rect.width / self.size  # Gen number of animation frames
        self.rotation_speed = 0.12  # time in seconds between animation frames

    def update(self):
        """Update animation"""
        # If time between frames elapsed - set image of the sprite to the next frame
        if self.timer < time():
            self.timer = time() + self.rotation_speed

            self.frame += 1
            # loop animation
            if self.frame == self.num_frames:
                self.frame = 0

            self.image = GFX().logo.subsurface((self.size * self.frame, 0, self.size, self.size))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
