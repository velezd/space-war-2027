class GameStatus():
    def __init__(self):
        self.game_running = False
        self.health = 100
        self.lives = 3
        self.score = 0
        self.high_scores = {'1':'10000',
                            '2':'9000',
                            '3':'8000',
                            '4':'7000',
                            '5':'6000',
                            '6':'5000',
                            '7':'4000',
                            '8':'3000',
                            '9':'2000'}

    def update(self):
        if self.lives == 0:
            self.game_running = False
