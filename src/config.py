from json import loads
from os import path
from utilities import singleton


@singleton
class CFG():
    """A class to store all settings"""

    def __init__(self):
        """Init the game's settings"""
        # Paths
        self.path_gfx = '../gfx/'
        self.path_fonts = '../gfx/fonts/'
        self.path_bg = '../gfx/backgrounds'
        self.path_bg_menu = '../gfx/backgrounds/menu'
        self.path_sfx = '../sfx/'
        self.path_music = '../sfx/music/'
        self.path_levels = '../levels/'
        self.path_settings = '../settings.json'
        self.path_save = '../save.json'

        # Screen settings
        self.screen_width = 1024
        self.screen_height = 768
        self.fullscreen = False
        self.scaling = True
        self.int_screen_width = 600
        self.int_screen_height = 300
        self.int_scale_width = 0
        self.int_scale_height = 0
        self.bg_color = (0,0,0)

        # Player ship settings
        self.ship_speed = 0.5

        # Player bullet settings
        self.bullet_speed = 0.75
        self.bullet_count = 10

        # Fonts
        self.font_main = path.join(self.path_fonts, 'PressStart2P.ttf')

        # Game settings
        self.start_level = 'level1.json'
        self.start_lives = 3
        self.spawn_speed = 0.5
        self.level_width = 15

        # Enemy settings
        self.asteroid_small_speed = 0.15
        self.shifter_speed = 0.10

        self.load()

    def load(self):
        """ Load Game settings from file """
        try:
            with open(self.path_settings, 'r') as file:
                data = loads(file.read())

            self.screen_width = int(data['screen_width'])
            self.screen_height = int(data['screen_height'])
            if data['fullscreen'] == 1:
                self.fullscreen = True
            else:
                self.fullscreen = False

            if data['scaling'] == 1:
                self.scaling = True
            else:
                self.scaling = False

        except IOError:
            print 'Can\'t load game settings'
