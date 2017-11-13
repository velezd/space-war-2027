from pygame.sprite import Group, Sprite
from time import time
from random import randint, uniform, choice


class Shifter(Sprite):
    def __init__(self, s, gfx, pos_x):
        """Init shifter - slowly moving enemy, constantly evading left and right, shooting randomly"""
        super(Shifter, self).__init__()
        self.gfx = gfx
        self.movement_speed = s.shifter_speed

        self.image = self.gfx.shifter['r']

        # Set starting position
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = 0

        # Stats
        self.health = 60
        self.max_evasion = 48
        self.anim_frame = 'r'
        self.evasion_speed = 0.09
        self.start_x = self.rect.centerx
        self.position_x = float(pos_x)
        self.shooting = False
        self.shoot_chance = 100
        self.shoot_at = randint(1, self.shoot_chance)
        self.size = self.rect.height

    def update(self, dt):
        """Update movement, animation and shooting"""
        # move the asteroid
        self.rect.bottom += self.movement_speed * dt
        move = self.evasion_speed * dt
        self.position_x += self.evasion_speed * dt
        self.rect.centerx = self.position_x

        # if on the maximum of evasion maneuver - switch direction
        if (self.rect.centerx + move < self.start_x - self.max_evasion or
            self.rect.centerx + move > self.start_x + self.max_evasion):
            # change movement direction
            self.evasion_speed *= -1.0

            # select animation frame
            if self.evasion_speed < 0:
                self.anim_frame = 'l'
            else:
                self.anim_frame = 'r'

            # change sprite image
            self.image = self.gfx.shifter[self.anim_frame]

        # shooting
        if not self.shooting:
            if self.shoot_at == randint(1, self.shoot_chance):
                print "pew"
                self.shooting = True

    def hit(self):
        self.health -= 20