from pygame.sprite import Sprite
from gfx import GFX
from time import time
from config import CFG


class PickupShield(Sprite):
    def __init__(self, position):
        """
        Adds lives or score to player when touched, moves down the level.

        :param position: list x,y where pickup should spawn
        """
        super(PickupShield, self).__init__()
        self.animation = GFX().pickups['shield']
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        self.movement_speed = 0.1
        self.num_frames = len(self.animation)
        self.frame = 0
        self.timer = 0
        self.animation_speed = 0.1

    def update(self, dt):
        """ Update movement and animation """
        # If time between frames elapsed - set image of the sprite to the next frame
        if self.timer < time():
            self.timer = time() + self.animation_speed

            self.frame += 1
            # loop animation
            if self.frame == self.num_frames:
                self.frame = 0

            self.image = self.animation[self.frame]

        # move the asteroid
        self.rect.bottom += self.movement_speed * dt

        # remove pickup when off screen
        if self.rect.top > CFG().int_screen_height:
            self.kill()

    def pickup(self, status):
        """ Perform 'pickup process': add lives or score and remove pickup """
        if status.lives < CFG().max_lives:
            status.lives += 1
        else:
            status.score += 1000
        self.kill()