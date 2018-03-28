from pygame import image, mask, transform, font
import tarfile
from os import path
from utilities import singleton
from config import CFG


@singleton
class GFX():
    """Inits and stores all graphics"""
    def __init__(self):
        # -- Loading images --
        # Player ship
        temp = image.load(path.join(CFG().path_gfx, 'ship0.png')).convert_alpha()
        size = temp.get_rect().height
        self.ship = {'c_0': temp.subsurface((0,0,size,size)),
                     'c_1': temp.subsurface((size,0,size,size)),
                     'l_0': temp.subsurface((size*2,0,size,size)),
                     'l_1': temp.subsurface((size*3,0,size,size)),
                     'r_0': temp.subsurface((size*4,0,size,size)),
                     'r_1': temp.subsurface((size*5,0,size,size))}

        # Enemy shifter
        temp = image.load(path.join(CFG().path_gfx, 'enemies/shifter.png')).convert_alpha()
        size = temp.get_rect().height
        self.shifter = {'c': temp.subsurface((size,0,size,size)),
                        'l': temp.subsurface((0, 0, size, size)),
                        'r': temp.subsurface((size*2, 0, size, size))}

        # Asteroids
        self.asteroids = []
        temp = [image.load(path.join(CFG().path_gfx, 'enemies/asteroid0.png')).convert_alpha(),
                image.load(path.join(CFG().path_gfx, 'enemies/asteroid1.png')).convert_alpha()]
        for img in temp:
            self.asteroids.append(self.load_animation(img))

        # Bosses
        self.boss1 = []
        temp = image.load(path.join(CFG().path_gfx, 'enemies/boss1.png')).convert_alpha()
        self.boss1 = {'down': [temp.subsurface(0,0,128,128),
                               temp.subsurface(128,0,128,128),
                               temp.subsurface(256,0,128,128),
                               temp.subsurface(384,0,128,128)],
                      'right': [temp.subsurface(512,0,128,128),
                                temp.subsurface(640, 0, 128, 128)],
                      'up': [temp.subsurface(768,0,128,128),
                             temp.subsurface(896,0,128,128),
                             temp.subsurface(1024,0,128,128),
                             temp.subsurface(1152,0,128,128)]}

        # Bullets
        self.bullets = [image.load(path.join(CFG().path_gfx, 'bullet.png')).convert_alpha(),
                        image.load(path.join(CFG().path_gfx, 'enemy_bullet1.png')).convert_alpha(),
                        image.load(path.join(CFG().path_gfx, 'enemy_bullet2.png')).convert_alpha()]
        self.bullet = image.load(path.join(CFG().path_gfx, 'bullet.png')).convert_alpha()
        self.enemy_bullet1 = image.load(path.join(CFG().path_gfx, 'enemy_bullet1.png')).convert_alpha()
        self.enemy_bullet2 = image.load(path.join(CFG().path_gfx, 'enemy_bullet2.png')).convert_alpha()

        # Effects
        self.fx_hits = [self.load_animation(image.load(path.join(CFG().path_gfx, 'effects/hit1.png')).convert_alpha()),
                        self.load_animation(image.load(path.join(CFG().path_gfx, 'effects/hit2.png')).convert_alpha()),
                        self.load_animation(image.load(path.join(CFG().path_gfx, 'effects/hit3.png')).convert_alpha())]
        self.fx_explosion = [self.load_animation(image.load(path.join(CFG().path_gfx,
                                                                      'effects/explosion2.png')).convert_alpha()),
                             self.load_animation(image.load(path.join(CFG().path_gfx,
                                                                      'effects/explosion3.png')).convert_alpha())]

        tmp = image.load(path.join(CFG().path_effects, 'player_shield.png')).convert_alpha()
        self.fx_player_shield = self.load_animation(tmp)

        # Story images
        self.story = self.load_story()

        # Backgrounds
        self.background = {}
        tmp = image.load(path.join(CFG().path_bg, 'background1.png')).convert()
        self.background['galaxy'] = transform.scale(tmp, (CFG().int_screen_width, CFG().int_screen_width))

        self.menu_background = {'front': image.load(path.join(CFG().path_bg_menu, 'ship_med_front.png')).convert_alpha(),
                                'back': image.load(path.join(CFG().path_bg_menu, 'ship_big_back.png')).convert_alpha()}

        # Misc
        tmp = image.load(path.join(CFG().path_gfx, 'progressbar.png')).convert()
        self.progressbar = [tmp.subsurface(0, 0, 16, 4), tmp.subsurface(16, 0, 16, 4)]

        tmp = image.load(path.join(CFG().path_gfx, 'hud_lives.png')).convert_alpha()
        self.hud_lives = self.load_animation(tmp)

        self.logo = image.load(path.join(CFG().path_gfx, 'logo.png')).convert_alpha()

        # -- Creating masks --
        self.ship_mask = {'c_0': mask.from_surface(self.ship['c_0']),
                          'c_1': mask.from_surface(self.ship['c_1']),
                          'l_0': mask.from_surface(self.ship['l_0']),
                          'l_1': mask.from_surface(self.ship['l_1']),
                          'r_0': mask.from_surface(self.ship['r_0']),
                          'r_1': mask.from_surface(self.ship['r_1'])}

        self.shifter_mask = {'c': mask.from_surface(self.shifter['c']),
                             'l': mask.from_surface(self.shifter['l']),
                             'r': mask.from_surface(self.shifter['r'])}

        self.boss1_mask = {}
        for x in self.boss1.keys():
            temp = []
            for img in self.boss1[x]:
                temp.append(mask.from_surface(img))
            self.boss1_mask[x] = temp

        self.asteroids_mask = []
        for asteroid in self.asteroids:
            list = []
            for frame in asteroid:
                list.append(mask.from_surface(frame))
            self.asteroids_mask.append(list)

        self.bullets_mask = []
        for bullet in self.bullets:
            self.bullets_mask.append(mask.from_surface(bullet))

        self.bullet_mask = mask.from_surface(self.bullet)
        self.enemy_bullet1_mask = mask.from_surface(self.enemy_bullet1)

    def load_animation(self, img):
        """ Splits image into animation frames and returns them as a list """
        size = img.get_rect()
        list = []

        for frame in range(size.width / size.height):
            list.append(img.subsurface(size.height * frame, 0, size.height, size.height))

        return list

    def load_story(self):
        '''
        Loads all story images from story.pak (tar.gz file)
        :return: Dictionary {'filename w/o extension': image}
        '''
        story = {}
        with tarfile.open(path.join(CFG().path_gfx, 'story/story.pak'), 'r:gz') as storytar:
            for file in storytar.getnames():
                name = file.split('.')[0]
                story[name] = image.load(storytar.extractfile(file)).convert()
        return story


class Text():
    """Manages and draws one font"""
    def __init__(self, screen, name, size, color, antialias=False):
        self.antialias = antialias
        self.font = font.Font(name, size)
        self.color = color
        self.screen = screen

    def write(self, text, x, y, color=None, origin=''):
        """Render text and blit it to screen"""
        if not color:
            color = self.color

        img = self.font.render(text, self.antialias, color)

        if origin == 'center':
            rect = img.get_rect()
            x = x - (rect.width / 2)
            y = y - (rect.height / 2)

        self.screen.blit(img, (x,y))
