from json import dumps, loads


class GameStatus():
    """Class for keeping game status and high scores"""
    def __init__(self):
        self.game_running = False
        self.health = 100
        self.lives = 3
        self.score = 0
        self.level = 1
        self.high_scores = [['1', '10000'],
                            ['2', '9000'],
                            ['3', '8000'],
                            ['4', '7000'],
                            ['5', '6000'],
                            ['6', '5000'],
                            ['7', '4000'],
                            ['8', '3000'],
                            ['9', '2000']]

    def reset(self):
        self.health = 100
        self.lives = 3
        self.score = 0
        self.level = 1

    def update(self):
        if self.lives == 0:
            self.game_running = False

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
