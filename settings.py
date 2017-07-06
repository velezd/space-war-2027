class Settings():
    """A class to store all settings"""

    def __init__(self):
        """Init the game's settings"""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
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
        self.level_width = 15
        # Enemy settings
        self.asteroid_small_speed = 0.15