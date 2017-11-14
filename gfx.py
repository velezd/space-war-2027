import pygame


class GFX():
    """Inits and stores all graphics"""
    def __init__(self, s):
        # -- Loading images --

        # Player ship
        temp = pygame.image.load('gfx/ship0.png').convert_alpha()
        size = temp.get_rect().height
        self.ship = {'c_0': temp.subsurface((0,0,size,size)),
                     'c_1': temp.subsurface((size,0,size,size)),
                     'l_0': temp.subsurface((size*2,0,size,size)),
                     'l_1': temp.subsurface((size*3,0,size,size)),
                     'r_0': temp.subsurface((size*4,0,size,size)),
                     'r_1': temp.subsurface((size*5,0,size,size))}

        # Enemy shifter
        temp = pygame.image.load('gfx/enemies/shifter.png').convert_alpha()
        size = temp.get_rect().height
        self.shifter = {'c': temp.subsurface((size,0,size,size)),
                        'l': temp.subsurface((0, 0, size, size)),
                        'r': temp.subsurface((size*2, 0, size, size))}

        # Asteroids
        temp = [pygame.image.load('gfx/enemies/asteroid0.png').convert_alpha(),
                pygame.image.load('gfx/enemies/asteroid1.png').convert_alpha()]

        # Separate image in to list of animation frames
        self.asteroids = []
        for image in temp:
            size = image.get_rect()
            list = []
            for frame in range(size.width/size.height):
                list.append(image.subsurface(size.height*frame, 0, size.height, size.height))
            self.asteroids.append(list)

        # Bullets
        self.bullet = pygame.image.load('gfx/bullet.png').convert_alpha()
        self.enemy_bullet1 = pygame.image.load('gfx/enemy_bullet1.png').convert_alpha()

        # Backgrounds
        self.background1 = pygame.image.load('gfx/backgrounds/background1.png').convert()
        self.background1 = pygame.transform.scale(self.background1, (s.int_screen_width, s.int_screen_width))

        self.menu_background = {'front': pygame.image.load('gfx/menu_background/ship_med_front.png').convert_alpha(),
                                'back': pygame.image.load('gfx/menu_background/ship_big_back.png').convert_alpha()}

        # Misc
        self.logo = pygame.image.load('gfx/logo.png').convert_alpha()

        # -- Creating masks --
        self.ship_mask = {'c_0': pygame.mask.from_surface(self.ship['c_0']),
                          'c_1': pygame.mask.from_surface(self.ship['c_1']),
                          'l_0': pygame.mask.from_surface(self.ship['l_0']),
                          'l_1': pygame.mask.from_surface(self.ship['l_1']),
                          'r_0': pygame.mask.from_surface(self.ship['r_0']),
                          'r_1': pygame.mask.from_surface(self.ship['r_1'])}

        self.shifter_mask = {'c': pygame.mask.from_surface(self.shifter['c']),
                             'l': pygame.mask.from_surface(self.shifter['l']),
                             'r': pygame.mask.from_surface(self.shifter['r'])}

        self.asteroids_mask = []
        for asteroid in self.asteroids:
            list = []
            for frame in asteroid:
                list.append(pygame.mask.from_surface(frame))
            self.asteroids_mask.append(list)

        self.bullet_mask = pygame.mask.from_surface(self.bullet)
        self.enemy_bullet1_mask = pygame.mask.from_surface(self.enemy_bullet1)


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
