from json import dumps, loads
from time import time


class GameStatus():
    """Class for keeping game status and high scores"""
    def __init__(self):
        self.game_running = False
        self.dead = False
        self.new_hs = False
        self.show_hs = False
        self.dead_timer = 0
        self.lives = 3
        self.score = 0
        self.level = 'level1.json'
        self.high_scores = [['1', 10000],
                            ['2', 9000],
                            ['3', 8000],
                            ['4', 7000],
                            ['5', 6000],
                            ['6', 5000],
                            ['7', 4000],
                            ['8', 3000],
                            ['9', 2000]]

    def reset(self):
        self.dead = False
        self.lives = 3
        self.score = 0
        self.level = 'level1.json'

    def update(self):
        # If dead and timer elapsed - stop game
        if self.dead and self.dead_timer < time():
            self.game_running = False
            return

        if self.lives == 0:
            # Add score to high scores - if high enough
            if self.score > self.high_scores[-1][1]:
                self.new_hs = True

            self.lives = 3
            self.dead = True
            self.show_hs = True
            self.dead_timer = time() + 3

    def save(self):
        """ Save Game status to file """
        data = {'lives': self.lives,
                'score': self.score,
                'level': self.level,
                'hscores': self.high_scores}

        js_data = dumps(data, indent=4, separators=(',', ': '))

        try:
            with open('save.json', 'w') as file:
                file.write(js_data)
        except IOError:
            print 'Can\'t save game and high scores'

    def load(self):
        """ Load Game status from file """
        try:
            with open('save.json', 'r') as file:
                data = loads(file.read())

            self.lives = data['lives']
            self.score = data['score']
            self.level = data['level']
            self.high_scores = data['hscores']
        except IOError:
            print 'Can\'t load saved game and high scores'
