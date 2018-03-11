from pygame.sprite import Sprite
from time import time
from random import randint, uniform, choice
from gfx import GFX
from config import CFG


class Asteroid(Sprite):
    def __init__(self, pos_x):
        """Init asteroid - square sprite with random image and rotation speed"""
        super(Asteroid, self).__init__()
        self.movement_speed = CFG().asteroid_small_speed

        # Stats
        self.health = 100
        self.reward = 100

        # Select random asteroid image
        self.i = randint(0, len(GFX().asteroids)-1)
        self.image = GFX().asteroids[self.i][0]

        # Set starting position
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = 0

        self.size = self.rect.height
        self.timer = 0

        self.num_frames = len(GFX().asteroids[self.i])    # Gen number of animation frames
        self.frame = randint(0, self.num_frames-1)   # Current frame number of animation - set random one
        self.rotation_speed = uniform(0.08, 0.2)     # time in seconds between animation frames
        self.direction = choice([1, -1])

        self.image = GFX().asteroids[self.i][self.frame]
        self.mask = GFX().asteroids_mask[self.i][self.frame]

    def update(self, dt, enemy_bullets, ship):
        """Update movement and animation"""
        # If time between frames elapsed - set image of the sprite to the next frame
        if self.timer < time():
            self.timer = time() + self.rotation_speed

            self.frame += self.direction
            # loop animation
            if self.frame == self.num_frames:
                self.frame = 0
            if self.frame == -1:
                self.frame = self.num_frames-1

            self.image = GFX().asteroids[self.i][self.frame]
            self.mask = GFX().asteroids_mask[self.i][self.frame]

        # move the asteroid
        self.rect.bottom += self.movement_speed * dt

    def hit(self):
        self.health -= 20