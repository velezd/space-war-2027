from time import time
from random import randint
from pygame.sprite import Group
from effects import stars
from config import CFG


class Background():
    """Manage and draw screen background"""
    def __init__(self, screen, image):
        self.background = image
        self.back_rect = self.background.get_rect()
        self.back_rect.centerx = randint(0, CFG().int_screen_width)
        self.back_rect.bottom = 0
        self.back_pos_y = 0.0
        self.back_speed = 0.03

        self.screen = screen
        self.stars = Group()
        stars.generate_init_stars(self.stars, 20, self.screen, 180)
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
            self.stars.add(stars.Star(self.screen, 180))

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.background, self.back_rect)

        for star in self.stars.sprites():
            star.draw()
