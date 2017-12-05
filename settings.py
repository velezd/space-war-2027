from json import loads


class Settings():
    """A class to store all settings"""

    def __init__(self):
        """Init the game's settings"""
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
        self.font_main = './fonts/PressStart2P.ttf'

        # Game settings
        self.start_level = 1
        self.spawn_speed = 0.5
        self.level_width = 15

        # Enemy settings
        self.asteroid_small_speed = 0.15
        self.shifter_speed = 0.10

        self.load()

    def load(self):
        """ Load Game settings from file """
        try:
            with open('settings.json', 'r') as file:
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
