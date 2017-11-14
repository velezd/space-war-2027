from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets from the ship"""

    def __init__(self, s, ship, gfx):
        super(Bullet, self).__init__()

        # Create bullet at the correct position
        self.image = gfx.bullet
        self.mask = gfx.bullet_mask
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

    def blitme(self, screen):
        """Draw the bullet"""
        screen.blit(self.image, self.rect)


class EnemyBullet(Sprite):
    """A class to manage enemy bullets"""

    def __init__(self, s, enemy, gfx, speed):
        super(EnemyBullet, self).__init__()

        # Create bullet at the correct position
        self.image = gfx.enemy_bullet1
        self.mask = gfx.enemy_bullet1_mask
        self.rect = self.image.get_rect()
        self.rect.centerx = enemy.rect.centerx
        self.rect.bottom = enemy.rect.bottom

        # Attributes
        self.pos_y = float(self.rect.y)
        self.speed = speed

    def update(self, dt):
        """Move the bullet on screen"""
        self.pos_y += self.speed * dt
        self.rect.y = self.pos_y

    def blitme(self, screen):
        """Draw the bullet"""
        screen.blit(self.image, self.rect)