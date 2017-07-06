import pygame


class GFX():
    """Inits and stores all graphics"""
    def __init__(self, s):
        self.logo = pygame.image.load('gfx/logo.png').convert_alpha()

        self.ship = {'c_0': pygame.image.load('gfx/ship/ship_c_0.png').convert_alpha(),
                     'c_1': pygame.image.load('gfx/ship/ship_c_1.png').convert_alpha(),
                     'l_0': pygame.image.load('gfx/ship/ship_l_0.png').convert_alpha(),
                     'l_1': pygame.image.load('gfx/ship/ship_l_1.png').convert_alpha(),
                     'r_0': pygame.image.load('gfx/ship/ship_r_0.png').convert_alpha(),
                     'r_1': pygame.image.load('gfx/ship/ship_r_1.png').convert_alpha()
                     }
        self.asteroid = [pygame.image.load('gfx/asteroid0.png').convert_alpha(),
                         pygame.image.load('gfx/asteroid1.png').convert_alpha()]

        self.menu_background = {'front': pygame.image.load('gfx/menu_background/ship_med_front.png').convert_alpha(),
                                'back': pygame.image.load('gfx/menu_background/ship_big_back.png').convert_alpha()}

        self.bullet = pygame.image.load('gfx/bullet.bmp').convert()
        self.bullet.set_colorkey((0, 255, 0))
        # Backgrounds
        self.background1 = pygame.image.load('gfx/background1.bmp').convert()
        self.background1 = pygame.transform.scale(self.background1, (s.int_screen_width, s.int_screen_width))


class Text():
    """Manages and draws one font"""
    def __init__(self, screen, font, size, color, antialias=False):
        self.antialias = antialias
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.screen = screen

    def write(self, text, x, y, color=None, origin=''):
        """Render text and blit it to screen"""
        if not color:
            color = self.color

        image = self.font.render(text, self.antialias, color)

        if origin == 'center':
            rect = image.get_rect()
            x = x - (rect.width / 2)
            y = y - (rect.height / 2)

        self.screen.blit(image, (x,y))
