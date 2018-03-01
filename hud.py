from gfx import Text


class HUD():
    def __init__(self, status, s, gfx, screen, clock):
        self.status = status
        self.screen = screen
        self.rect = screen.get_rect()
        self.s = s
        self.gfx = gfx
        self.clock = clock
        self.text = Text(self.screen, s.font_main, 16, (255, 255, 255))

    def draw(self):
        if self.status.game_running:
            self.text.write(str(self.status.lives), 5, 45)
            self.text.write(str(self.status.score), 5, 65)

            if self.status.dead:
                self.text.write('Game Over', self.rect.width/2, self.rect.height/2, origin='center')

        self.text.write(str(int(self.clock.get_fps())), 5, 5)
