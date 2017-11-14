from time import time
from pygame.sprite import Group, Sprite
from enemies import asteroid, shifter


class Level():
    def __init__(self, s, gfx, int_screen):
        self.s = s
        self.gfx = gfx
        self.int_screen = int_screen
        self.level = []
        self.timer = 0
        self.enemies = Group()

        with open('levels/' + str(s.start_level), 'r') as file:
            self.level = file.read().splitlines()

    def update(self, dt, enemy_bullets):
        if self.timer < time():
            print self.s.spawn_speed * dt
            self.timer = time() + self.s.spawn_speed * dt
            if len(self.level) != 0:
                line = self.level.pop(-1)
                position = 0
                for char in line:
                    position += 1
                    # If there is enemy calculate it's x position
                    if char != '-':
                        spacing = self.s.int_screen_width / self.s.level_width
                        pos_x = spacing * position - spacing / 2

                    if char == 'a':
                        self.enemies.add(asteroid.Asteroid(self.s, self.gfx, pos_x))

                    if char == 's':
                        self.enemies.add(shifter.Shifter(self.s, self.gfx, pos_x))

        self.enemies.update(dt, enemy_bullets)

    def draw(self):
        self.enemies.draw(self.int_screen)
