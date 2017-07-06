from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets from the ship"""

    def __init__(self, s, ship, gfx):
        super(Bullet, self).__init__()

        # Create bullet at the correct position
        self.image = gfx.bullet
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
