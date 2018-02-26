from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame.mask import from_surface
from math import cos, sin, radians, asin, degrees, sqrt


class Bullet(Sprite):
    """A class to manage bullets from the ship"""

    def __init__(self, s, ship, gfx):
        super(Bullet, self).__init__()

        # Create bullet at the correct position
        self.image = gfx.bullets[0]
        self.mask = gfx.bullets_mask[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top

        # Attributes
        self.pos_y = float(self.rect.y)
        self.speed = s.bullet_speed

    def update(self, dt):
        """Move the bullet on screen"""
        self.pos_y -= self.speed * dt
        self.rect.y = self.pos_y

        if self.rect.bottom <= 0:
            self.kill()

    def blitme(self, screen):
        """Draw the bullet"""
        screen.blit(self.image, self.rect)


class EnemyBullet(Sprite):
    """A class to manage enemy bullets"""
    def __init__(self, position, gfx, speed, look=1, target=None):
        """ Create and aim bullet

        Target angle is -90 left, 0 straight down, 90 right
        :param position: Starting position: Sprite or [x, y]
        :param gfx: game graphics lib
        :param speed: speed of the bullet
        :param look: index of the bullet image
        :param target: Target to aim at None/int angle/[x,y]
        """
        super(EnemyBullet, self).__init__()

        # Set selected image, mask and rect
        self.image = gfx.bullets[look]
        self.mask = gfx.bullets_mask[look]
        self.rect = self.image.get_rect()

        # Set starting position
        if isinstance(position, Sprite):
            self.rect.centerx = position.rect.centerx
            self.rect.bottom = position.rect.bottom
        else:
            self.rect.centerx = position[0]
            self.rect.centery = position[1]

        # Attributes
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.speedx = 0
        self.speedy = 0
        self.angle = 0

        if target is None:
            self.speedy = speed
        else:
            if isinstance(target, list):
                # Calculate angle to target
                a = target[0] - self.rect.x
                b = target[1] - self.rect.y
                c = sqrt(a ** 2 + b ** 2)
                self.angle = degrees(asin(a / c))
            else:
                self.angle = target

            # Rotate bullet image
            if self.angle != 0:
                self.image = rotate(self.image, self.angle)
                self.mask = from_surface(self.image)
                self.rect = self.image.get_rect()

            # Perform vectoring based on angle
            self.angle += 90
            self.angle = radians(self.angle)
            self.speedx = cos(self.angle) * speed * -1
            self.speedy = sin(self.angle) * speed

    def update(self, dt):
        """Calculate position and move bullet"""
        if self.speedx != 0:
            self.pos_x += self.speedx * dt
            self.rect.x = self.pos_x

        self.pos_y += self.speedy * dt
        self.rect.y = self.pos_y

    def blitme(self, screen):
        """Draw the bullet"""
        screen.blit(self.image, self.rect)
