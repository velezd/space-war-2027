from pygame.sprite import Group, Sprite
from time import time
from random import randint, uniform, choice


class Asteroid(Sprite):
    def __init__(self, s, gfx, pos_x):
        """Init asteroid - square sprite with random image and rotation speed"""
        super(Asteroid, self).__init__()
        self.gfx = gfx
        self.movement_speed = s.asteroid_small_speed

        # Stats
        self.health = 100

        # Select random asteroid image
        self.i = randint(0, len(gfx.asteroid)-1)
        self.image = self.gfx.asteroid[self.i].subsurface((0,0,32,32))

        # Set starting position
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = 0

        self.size = self.rect.height
        self.timer = 0

        self.num_frames = self.gfx.asteroid[self.i].get_rect().width / self.size    # Gen number of animation frames
        self.frame = randint(0, self.num_frames-1)   # Current frame number of animation - set random one
        self.rotation_speed = uniform(0.08, 0.2)     # time in seconds between animation frames
        self.direction = choice([1, -1])

    def update(self, dt):
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

            self.image = self.gfx.asteroid[self.i].subsurface((self.size * self.frame, 0, self.size, self.size))

        # move the asteroid
        self.rect.bottom += self.movement_speed * dt

    def hit(self):
        self.health -= 20