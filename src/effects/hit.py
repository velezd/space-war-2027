from pygame.sprite import Sprite
from time import time
from random import randint
from gfx import GFX


class Hit(Sprite):
    """ Hit effect sprite """

    def __init__(self, position):
        super(Hit, self).__init__()

        self.animation = GFX().fx_hits[randint(0, len(GFX().fx_hits) - 1)]
        self.animation_speed = 0.05
        self.frame = 0
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.timer = 0

    def update(self, dt):
        """ Update animation """
        if time() > self.timer:
            if self.frame < len(self.animation):
                self.image = self.animation[self.frame]
                self.timer = time() + self.animation_speed
                self.frame += 1
            else:
                self.kill()

    def blitme(self, screen):
        """ Draw the effect """
        screen.blit(self.image, self.rect)


class Explosion(Hit):
    def __init__(self, position):
        super(Explosion,self).__init__(position)
        self.animation = GFX().fx_explosion[randint(0, len(GFX().fx_explosion) - 1)]
        self.animation_speed = 0.07

        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
