from pygame.sprite import Group, Sprite
from time import time
from random import randint, uniform, choice
from bullet import BossBullet1


class Boss1(Sprite):
    def __init__(self, s, gfx):
        """Init asteroid - square sprite with random image and rotation speed"""
        super(Boss1, self).__init__()
        self.s = s
        self.gfx = gfx

        self.img_down = self.gfx.boss1['down']
        self.img_right = self.gfx.boss1['right']
        self.img_up = self.gfx.boss1['up']

        self.mask_down = self.gfx.boss1_mask['down']
        self.mask_right = self.gfx.boss1_mask['right']
        self.mask_up = self.gfx.boss1_mask['up']

        self.image = self.img_down[0]
        self.mask = self.mask_down[0]
        self.rect = self.image.get_rect()
        self.pos_x = 96.0
        self.pos_y = -64.0
        self.moving = 'down'

        self.next_stage = False
        self.stage = 1
        self.health = 5000

        self.shoot_timer1 = 0
        self.shoot_timer2 = 0
        self.canon = 1

        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

    def update(self, dt, enemy_bullets):
        """Update movement and animation"""
        spd_y = 0
        spd_x = 0
        # First stage of the boss
        if self.stage == 1:
            # When under x health switch next stage flag
            if self.health < 2500 and not self.next_stage:
                self.next_stage = True
            # Go down
            if self.moving == 'down':
                if self.pos_y >= 60:
                    self.moving = 'right'
                    self.image = self.img_right[0]
                    self.mask = self.mask_right[0]
                elif self.pos_y >= 55:
                    self.image = self.img_down[3]
                    self.mask = self.mask_down[3]
                    spd_y = 0.02
                elif self.pos_y >= 50:
                    self.image = self.img_down[2]
                    self.mask = self.mask_down[2]
                    spd_y = 0.05
                elif self.pos_y >= 45:
                    self.image = self.img_down[1]
                    self.mask = self.mask_down[1]
                    spd_y = 0.07
                else:
                    spd_y = 0.1

            # go right and shoot
            if self.moving == 'right':
                if self.pos_x >= 504:
                    self.moving = 'up'
                elif self.pos_x >= 500:
                    self.image = self.img_right[0]
                    self.mask = self.mask_right[0]
                elif self.pos_x >= 100:
                    self.image = self.img_right[1]
                    self.mask = self.mask_right[1]
                spd_x = 0.05

                # Shooting
                if time() > self.shoot_timer1:
                    position = [self.rect.left + 34 + (12 * self.canon),
                                self.rect.centery + 50]
                    enemy_bullets.add(BossBullet1(self.s, position, self.gfx, 0.15))

                    self.canon += 1
                    if self.canon > 4:
                        self.canon = 1
                        self.shoot_timer1 = time() + 1
                    else:
                        self.shoot_timer1 = time() + 0.25

            # go up
            if self.moving == 'up':
                if self.pos_y <= -64:
                    if self.next_stage:
                        self.stage = 2
                        self.next_stage = False
                    else:
                        self.image = self.img_down[0]
                        self.mask = self.mask_down[0]
                        self.pos_x = 96.0
                        self.pos_y = -64.0
                        self.moving = 'down'
                elif self.pos_y <= 45:
                    self.image = self.img_up[3]
                    self.mask = self.mask_up[3]
                    spd_y = -0.1
                elif self.pos_y <= 50:
                    self.image = self.img_up[2]
                    self.mask = self.mask_up[2]
                    spd_y = -0.07
                elif self.pos_y <= 55:
                    self.image = self.img_up[1]
                    self.mask = self.mask_up[1]
                    spd_y = -0.05
                else:
                    self.image = self.img_up[0]
                    self.mask = self.mask_up[0]
                    spd_y = -0.02
        if self.stage == 2:
            spd_y = 0.2

        # calculate movement
        self.pos_x += spd_x * dt
        self.pos_y += spd_y * dt
        # apply movement
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

    def hit(self):
        self.health -= 20