import pygame
from gfx import Text
from config import CFG
from events import Events


class HSEntry():
    """ Show 3 letter name entry dialog """
    def __init__(self, int_screen, status):
        """ Init dialog

        :param int_screen: Internal screen
        :param status: Game status
        :param s: Game settings
        """
        self.int_screen = int_screen
        self.status = status
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!'
        self.name = ''
        self.cursor = 0
        self.done = False
        self.highlight_color = (100,100,100)
        self.name_position = [320,150]
        self.title = 'New high score!'
        self.title_position = [320,50]

        self.x = 50
        self.y = 220

        self.font1 = Text(self.int_screen, CFG().font_main, 16, (255, 255, 255))
        self.font2 = Text(self.int_screen, CFG().font_main, 40, (255, 255, 255))

        self.cursor_surf = pygame.Surface((20,20))
        self.cursor_surf.fill(self.highlight_color)
        self.cursor_rect = self.cursor_surf.get_rect()
        self.cursor_rect.top = self.y-3
        self.cursor_rect.left = self.x-3

        self.highlight_surf = pygame.Surface((130, 50))
        self.highlight_surf.fill(self.highlight_color)
        self.highlight_rect = self.highlight_surf.get_rect()
        self.highlight_rect.top = self.name_position[1] - 29
        self.highlight_rect.left = self.name_position[0] - 69

    def update(self):
        """ Check keyboard events and length of the name """
        if Events().right_pressed:
            if self.cursor < 26:
                self.cursor += 1
                self.cursor_rect.x += 20

        if Events().left_pressed:
            if self.cursor > 0:
                self.cursor -= 1
                self.cursor_rect.x -= 20

        if Events().fire2_pressed:
            if len(self.name) < 3:
                self.name = self.name + self.letters[self.cursor]
            else:
                self.status.high_scores.append([self.name, self.status.score])
                self.status.high_scores = sorted(self.status.high_scores, key=lambda x: x[1], reverse=True)
                self.status.high_scores.pop(-1)
                self.status.score = 0
                self.status.new_hs = False

        if Events().cancel_pressed:
            if len(self.name) > 0:
                self.name = self.name[:-1]

        if len(self.name) == 3:
            self.done = True
        elif self.done:
            self.done = False

    def draw(self):
        """ Draws dialog on internal screen """
        # Display highlight under selected letter on name
        if self.done:
            self.int_screen.blit(self.highlight_surf, self.highlight_rect)
        else:
            self.int_screen.blit(self.cursor_surf, self.cursor_rect)

        # Display title
        self.font1.write(self.title, self.title_position[0], self.title_position[1], origin='center')

        # Display name
        self.font2.write(self.name, self.name_position[0], self.name_position[1], origin='center')

        # Display alphabet
        x = self.x
        for letter in self.letters:
            self.font1.write(letter, x, self.y)
            x += 20


class HSDisplay():
    """ Show highscores """
    def __init__(self, int_screen, status):
        """ Init text, set dimensions

        :param int_screen: Internal screen
        :param status: Game status
        :param s: Game settings
        """
        self.int_screen = int_screen
        self.status = status
        self.font = Text(self.int_screen, CFG().font_main, 16, (255, 255, 255))
        self.y = 40
        self.spacing = 25
        self.x_name = 230
        self.x_score = 320

    def update(self):
        """ Check events """
        if Events().key_pressed:
            self.status.show_hs = False

    def draw(self):
        """ Draw highscores table """
        y = self.y
        for hs in self.status.high_scores:
            self.font.write(hs[0], self.x_name, y)
            self.font.write(str(hs[1]), self.x_score, y)
            y += self.spacing
