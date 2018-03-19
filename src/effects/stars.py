import pygame
from pygame.sprite import Sprite
from random import randint
from math import cos, sin, radians


class Star(Sprite):
    """ Class for running stars, for background or foreground """
    def __init__(self, screen, angle=0, position=None):
        """ Star(s Settings, screen Surface, angle int(0-359), position (x int,y int))
        Color and speed is random. Stars run towards defined angle:
              0
              |
        270 --+-- 90
              |
             180
        """
        super(Star, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        if position is None:
            # Figure out starting plane of stars
            if angle == 0:
                spawnx = randint(0, self.screen_rect.width)
                spawny = self.screen_rect.width
            elif angle == 90:
                spawnx = 0
                spawny = randint(0, self.screen_rect.height)
            elif angle == 180:
                spawnx = randint(0, self.screen_rect.width)
                spawny = 0
            elif angle == 270:
                spawnx = self.screen_rect.width
                spawny = randint(0, self.screen_rect.height)
            # from left to right
            elif 0 < angle < 180:
                plane = randint(0, self.screen_rect.width + self.screen_rect.height)
                # from bottom and left
                if angle < 90:
                    if plane > self.screen_rect.height:
                        spawnx = plane - self.screen_rect.height
                        spawny = self.screen_rect.height
                    else:
                        spawnx = 0
                        spawny = plane
                # from top and left
                else:
                    if plane > self.screen_rect.height:
                        spawnx = plane - self.screen_rect.height
                        spawny = 0
                    else:
                        spawnx = 0
                        spawny = plane
            # from right to left
            elif 180 < angle < 360:
                plane = randint(0, self.screen_rect.width + self.screen_rect.height)
                # from top and right
                if angle < 270:
                    if plane > self.screen_rect.height:
                        spawnx = plane - self.screen_rect.height
                        spawny = 0
                    else:
                        spawnx = self.screen_rect.width
                        spawny = plane
                # from bottom and right
                else:
                    if plane > self.screen_rect.height:
                        spawnx = plane - self.screen_rect.height
                        spawny = self.screen_rect.height
                    else:
                        spawnx = self.screen_rect.width
                        spawny = plane
            # Fallback - beam from center
            else:
                spawnx = self.screen_rect.centerx
                spawny = self.screen_rect.centery
        # Spawn on custom position
        else:
            spawnx = position[0]
            spawny = position[1]

        # Init star
        self.image = pygame.Surface((2, 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = spawnx
        self.rect.centery = spawny
        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.centery
        # Random color
        r = randint(128, 255)
        self.image.fill((r,r,r))
        # Vectoring
        speed = float(randint(10, 20))/100
        angle -= 90
        angle = radians(angle)
        self.speedx = cos(angle) * speed
        self.speedy = sin(angle) * speed

    def update(self, dt):
        """ Move star """
        self.pos_x += self.speedx * dt
        self.pos_y += self.speedy * dt
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        if not self.on_screen():
            self.kill()

    def on_screen(self):
        """ Returns True if star is till visible on defined surface """
        is_on = True
        if self.rect.bottom < self.screen_rect.top:
            is_on = False
        if self.rect.top > self.screen_rect.bottom:
            is_on = False
        if self.rect.right < self.screen_rect.left:
            is_on = False
        if self.rect.left > self.screen_rect.right:
            is_on = False

        return is_on


def generate_init_stars(group, num, screen, angle):
    """ Spawns defined number of stars randomly on screen,
        used for initial population of the screen """
    rect = screen.get_rect()
    for n in range(num):
        x = randint(0, rect.width)
        y = randint(0, rect.height)
        group.add(Star(screen, angle, (x,y)))
