from pygame.sprite import Sprite
from time import time
from bullet import EnemyBullet
from math import cos, sin, radians
from utilities import rt_angle, isclose
import pygame
from gfx import GFX
from sfx import SFX


class Boss(Sprite):
    """ Boss sprite parent class """
    def __init__(self):
        """ Init enemy boss """
        super(Boss, self).__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image = pygame.Surface((0, 0))
        self.mask = pygame.Mask((0, 0))
        # Movement variables
        self.pos_x = 0
        self.pos_y = 0
        self.speedx = 0
        self.speedy = 0
        self.animation_speed = 0
        self.animation_frame = 0
        # Animation waypoint in absolute coordinates
        self.target_x = 0
        self.target_y = 0

    def init_animation(self, animation_start):
        """ Clear movement/animation variables

        :param animation_start: Absolute coordinates [x,y]
        :return: Nothing
        """
        self.pos_x = animation_start[0]
        self.pos_y = animation_start[1]
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y
        self.animation_frame = 0

    def calculate_movement(self, animation):
        """ Calculates movement speeds x,y from the relative position of the next animation waypoint

        :param animation: List of animation frames
        :return: Nothing
        """
        frame = animation[self.animation_frame]

        self.target_x = self.rect.centerx + frame[0]
        self.target_y = self.rect.centery + frame[1]

        # Get angle to target
        angle = rt_angle(frame[0], frame[1])

        # Perform vectoring based on angle
        angle += 90
        angle = radians(angle)
        self.speedx = cos(angle) * self.animation_speed * -1
        self.speedy = sin(angle) * self.animation_speed

        # Going up
        if frame[1] < 0:
            self.speedy *= -1

    def animate(self, animation, animation_start, dt):
        """ Plays animation - moves sprite, changes image and mask

        :param animation: List of animation frames
        :param animation_start: Starting point of the animation [x,y]
        :param dt: time between frames
        :return: True if animation is ended, False if not
        """
        anim_end = False
        # if reached animation waypoint
        if isclose(self.target_x, self.pos_x, 0.10, 0.8) and isclose(self.target_y, self.pos_y, 0.10, 0.8):
            self.animation_frame += 1

            if len(animation) == self.animation_frame:
                anim_end = True
                # loop animation
                self.init_animation(animation_start)

            # Set new image and mask
            self.image = animation[self.animation_frame][2]
            self.mask = animation[self.animation_frame][3]
            # Calculate new movement speedssfx
            self.calculate_movement(animation)

        # calculate movement
        self.pos_x += self.speedx * dt
        self.pos_y += self.speedy * dt
        # apply movement
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        return anim_end


class Boss1(Boss):
    def __init__(self):
        """ Init enemy boss """
        super(Boss1, self).__init__()
        # Properties
        self.stage = 1
        self.next_stage = None
        self.health = 4000
        self.reward = 2000
        self.animation_speed = 0.06
        # Shooting
        self.shoot_timer1 = 0
        self.canon = 1

        # Set images and rect
        self.img_down = GFX().boss1['down']
        self.img_right = GFX().boss1['right']
        self.img_up = GFX().boss1['up']

        self.mask_down = GFX().boss1_mask['down']
        self.mask_right = GFX().boss1_mask['right']
        self.mask_up = GFX().boss1_mask['up']

        self.image = self.img_down[0]
        self.mask = self.mask_down[0]
        self.rect = self.image.get_rect()

        # Movement animations - relative waypoints for movement and image for that movement
        self.animation1_start = [96, -64]
        self.animation1 = [[0, 128, self.img_down[0], self.mask_down[0]],
                           [5, 20, self.img_down[1], self.mask_down[1]],
                           [10, 20, self.img_down[2], self.mask_down[2]],
                           [20, 10, self.img_down[3], self.mask_down[3]],
                           [20, 5, self.img_right[0], self.mask_right[0]],
                           [349, 0, self.img_right[1], self.mask_right[1]],
                           [20, -5, self.img_right[0], self.mask_right[0]],
                           [20, -10, self.img_up[0], self.mask_up[0]],
                           [10, -20, self.img_up[1], self.mask_up[1]],
                           [5, -20, self.img_up[2], self.mask_up[2]],
                           [0, -128, self.img_up[3], self.mask_up[3]]]

        self.animation2_start = [192, -64]
        self.animation2 = [[0, 32, self.img_down[0], self.mask_down[0]],
                           [5, 20, self.img_down[1], self.mask_down[1]],
                           [10, 20, self.img_down[2], self.mask_down[2]],
                           [20, 10, self.img_down[3], self.mask_down[3]],
                           [20, 5, self.img_right[0], self.mask_right[0]],
                           [154, 0, self.img_right[1], self.mask_right[1]],
                           [20, -5, self.img_right[0], self.mask_right[0]],
                           [20, -10, self.img_up[0], self.mask_up[0]],
                           [10, -20, self.img_up[1], self.mask_up[1]],
                           [5, -20, self.img_up[2], self.mask_up[2]],
                           [0, -32, self.img_up[3], self.mask_up[3]]]

        self.init_animation(self.animation1_start)
        self.calculate_movement(self.animation1)

    def update(self, dt, enemy_bullets, ship):
        """ Update movement, animation and shooting

        :param dt: time between frames
        :param enemy_bullets: Sprite group
        :param ship: Sprite - player
        :return: Nothing
        """
        # Stage 1
        if self.stage == 1:
            if self.animate(self.animation1, self.animation1_start, dt):
                if self.health < 2000:
                    self.stage = 2
                    self.init_animation(self.animation2_start)
                    self.calculate_movement(self.animation2)

            # Shooting
            if self.animation_frame == 5:
                if time() > self.shoot_timer1:
                    position = [self.rect.left + 34 + (12 * self.canon), self.rect.centery + 50]
                    target = [ship.rect.centerx, ship.rect.centery]
                    enemy_bullets.add(EnemyBullet(position, 0.15, 2, target))
                    SFX().blaster2.play()

                    self.canon += 1
                    if self.canon > 4:
                        self.canon = 1
                        self.shoot_timer1 = time() + 1
                    else:
                        self.shoot_timer1 = time() + 0.25

        # Stage 2
        elif self.stage == 2:
            self.animate(self.animation2, self.animation2_start, dt)

            # Shooting
            if self.animation_frame == 5:
                if time() > self.shoot_timer1:
                    enemy_bullets.add(EnemyBullet([self.rect.left + 46, self.rect.centery + 50], 0.15, 2, -30))
                    enemy_bullets.add(EnemyBullet([self.rect.left + 58, self.rect.centery + 50], 0.15, 2, -10))
                    enemy_bullets.add(EnemyBullet([self.rect.left + 70, self.rect.centery + 50], 0.15, 2, 10))
                    enemy_bullets.add(EnemyBullet([self.rect.left + 82, self.rect.centery + 50], 0.15, 2, 30))
                    SFX().blaster2.play()
                    self.shoot_timer1 = time() + 0.8

    def hit(self):
        self.health -= 20
