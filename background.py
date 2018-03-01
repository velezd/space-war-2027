import pygame
from time import time
from random import randint
from pygame.sprite import Group, Sprite
from effects import stars


class Background():
    """Manage and draw screen background"""
    def __init__(self, s, screen, image):
        self.s = s
        self.background = image
        self.back_rect = self.background.get_rect()
        self.back_rect.centerx = randint(0, s.int_screen_width)
        self.back_rect.bottom = 0
        self.back_pos_y = 0.0
        self.back_speed = 0.03

        self.screen = screen
        self.stars = Group()
        stars.generate_init_stars(self.stars, 20, self.s, self.screen, 180)
        self.gen_speed = 0.1

        # set timer
        self.timer = time() + self.gen_speed

    def update(self, dt):
        self.back_pos_y += self.back_speed * dt
        self.back_rect.bottom = self.back_pos_y

        self.stars.update(dt)

        # Add stars
        if self.timer < time():
            self.timer = time() + self.gen_speed
            self.stars.add(stars.Star(self.s, self.screen, 180))

        # Remove stars
        for star in self.stars:
            if not star.is_on(self.screen):
                self.stars.remove(star)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.background, self.back_rect)

        for star in self.stars.sprites():
            star.draw()

'''
class Star(Sprite):
    def __init__(self, s, screen):
        super(Star, self).__init__()

        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 2)
        self.rect.centerx = randint(0, s.int_screen_width)
        r = randint(128, 255)
        self.color = (r,r,r)
        self.speed = float(randint(5, 15))/100
        self.pos_y = 0.0

    def update(self, dt):
        self.pos_y += self.speed * dt
        self.rect.centery = self.pos_y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
'''
