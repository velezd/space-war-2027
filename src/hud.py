from gfx import Text, GFX
from config import CFG


class HUD():
    def __init__(self, status, screen, clock):
        self.status = status
        self.screen = screen
        self.rect = screen.get_rect()
        self.clock = clock
        self.text = Text(self.screen, CFG().font_main, 16, (255, 255, 255))

        bottom_border = CFG().screen_height - ((CFG().screen_height - CFG().int_scale_height) / 4)
        # Score position
        self.score_x = CFG().screen_width / 2
        self.score_y = bottom_border
        # Lives position
        self.lives_size = GFX().hud_lives[0].get_rect().width
        self.lives_x = 20
        self.lives_y = bottom_border - (self.lives_size/2)
        # Boss lives position
        self.boss_x = CFG().screen_width / 2
        self.boss_y = ((CFG().screen_height - CFG().int_scale_height) / 6)
        self.boss_rect = GFX().progressbar[0].get_rect()

    def draw(self):
        if self.status.game_running:
            self.draw_lives()
            self.draw_boss_lives()
            self.text.write(str(self.status.score).zfill(8), self.score_x, self.score_y, origin='center')

            if self.status.dead:
                self.text.write('Game Over', self.rect.width/2, self.rect.height/2, origin='center')

        if CFG().show_fps:
            self.text.write(str(int(self.clock.get_fps())), 5, 5)

    def draw_boss_lives(self):
        if self.status.boss_lives != 0:
            self.text.write('Boss', self.boss_x, self.boss_y, origin='center')
            lives = self.status.boss_lives
            x = self.boss_x - (self.boss_rect.width * 5 + 16)
            for a in range(10):
                if lives != 0:
                    self.screen.blit(GFX().progressbar[0], (x, self.boss_y + 25,
                                                            self.boss_rect.width, self.boss_rect.height))
                    lives -= 1
                else:
                    self.screen.blit(GFX().progressbar[1], (x, self.boss_y + 25,
                                                            self.boss_rect.width, self.boss_rect.height))
                x += 20

    def draw_lives(self):
        x = self.lives_x
        lives = self.status.lives
        for a in range(CFG().max_lives):
            if lives != 0:
                self.screen.blit(GFX().hud_lives[0], (x, self.lives_y, self.lives_size, self.lives_size))
                lives -= 1
            else:
                self.screen.blit(GFX().hud_lives[1], (x, self.lives_y, self.lives_size, self.lives_size))
            x += 22
