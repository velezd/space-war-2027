from pygame.sprite import Sprite
from time import time
from gfx import GFX


class PlayerShield(Sprite):
    """ Shield around player ship, that follows it """

    def __init__(self, ship):
        super(PlayerShield, self).__init__()

        self.ship = ship
        self.animation = GFX().fx_player_shield
        self.animation_speed = 0.05
        self.frame = 0
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.ship.rect.centerx
        self.rect.centery = self.ship.rect.centery
        self.timer = 0

    def update(self, dt):
        """ Update animation """
        self.rect.centerx = self.ship.rect.centerx
        self.rect.centery = self.ship.rect.centery

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