from os import path
from pygame import mixer
from config import CFG
from utilities import singleton


@singleton
class SFX():
    def __init__(self):
        # Sound effects
        self.blaster1 = mixer.Sound(path.join(CFG().path_sfx, 'blaster1.ogg'))
        self.blaster1.set_volume(CFG().sfx_volume)
        self.blaster2 = mixer.Sound(path.join(CFG().path_sfx, 'blaster2.ogg'))
        self.blaster2.set_volume(CFG().sfx_volume)
        self.boom1 = mixer.Sound(path.join(CFG().path_sfx, 'boom1.ogg'))
        self.boom1.set_volume(CFG().sfx_volume)
        # Music
        self.music = {}
        self.music['arpent'] = path.join(CFG().path_music, 'arpent.ogg')

    def music_play(self, song, loop=True):
        mixer.music.load(SFX().music[song])
        mixer.music.set_volume(CFG().music_volume)
        if loop:
            mixer.music.play(-1)
        else:
            mixer.music.play(0)

    def music_stop(self):
        mixer.music.stop()

    def is_music_playing(self):
        return mixer.music.get_busy()
