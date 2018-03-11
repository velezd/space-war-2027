from os import path
from pygame import mixer
from config import CFG
from utilities import singleton


@singleton
class SFX():
    def __init__(self):
        self.blaster1 = mixer.Sound(path.join(CFG().path_sfx, 'blaster1.ogg'))
        self.blaster2 = mixer.Sound(path.join(CFG().path_sfx, 'blaster2.ogg'))
        self.boom1 = mixer.Sound(path.join(CFG().path_sfx, 'boom1.ogg'))
        self.music = {}
        self.music['arpent'] = path.join(CFG().path_music, 'arpent.ogg')