import pygame


class SFX():
    def __init__(self):
        self.blaster1 = pygame.mixer.Sound('sfx/blaster1.ogg')
        self.blaster2 = pygame.mixer.Sound('sfx/blaster2.ogg')
        self.boom1 = pygame.mixer.Sound('sfx/boom1.ogg')
        self.music = {}
        self.music['arpent'] = 'sfx/music/arpent.ogg'