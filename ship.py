from time import time


class Ship():
    def __init__(self, screen, s, gfx):
        """Init the player ship and it's starting position"""
        self.screen = screen
        self.s = s
        self.gfx = gfx

        # load the ships image and get it's rect
        self.image = gfx.ship['c_0']
        self.mask = gfx.ship_mask['c_0']
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Start the ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Attributes
        self.pos_x = float(self.rect.centerx)
        self.shooting_timer = 0

        # Flags
        self.moving_left = False
        self.moving_right = False
        self.moving_center = False # Used for resetting ship image
        self.shooting = False

    def blitme(self):
        """Draw the ship"""
        self.screen.blit(self.image, self.rect)

    def update(self, dt):
        """Updates ship movement and graphics"""
        # After shooting timer runs out remove shooting flag and reset ship image
        if self.shooting_timer < time():
            self.shooting = False
            self.moving_center = True

        # Calculating ship movement and setting correct image
        if self.moving_left and self.rect.left > 0:
            self.pos_x -= self.s.ship_speed * dt
            self.image = self.gfx.ship['l_0']
            self.mask = self.gfx.ship_mask['l_0']
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.pos_x += self.s.ship_speed * dt
            self.image = self.gfx.ship['r_0']
            self.mask = self.gfx.ship_mask['r_0']
        elif self.moving_center:
            self.image = self.gfx.ship['c_0']
            self.mask = self.gfx.ship_mask['c_0']
            self.moving_center = False

        # if shooting use special ship image
        if self.shooting:
            if self.moving_left:
                self.image = self.gfx.ship['l_1']
            elif self.moving_right:
                self.image = self.gfx.ship['r_1']
            else:
                self.image = self.gfx.ship['c_1']

        # Apply ship movement
        self.rect.centerx = self.pos_x

