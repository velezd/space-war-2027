from time import time
from pygame.sprite import Group, Sprite
from enemies import asteroid, shifter, boss


class Level():
    def __init__(self, s, gfx, int_screen):
        self.s = s
        self.gfx = gfx
        self.int_screen = int_screen
        self.level = []
        self.timer = 0
        self.enemies = Group()
        self.enemy_hold = False

        with open('levels/' + str(s.start_level), 'r') as file:
            self.level = file.read().splitlines()

    def update(self, dt, enemy_bullets, ship):
        # Enemy spawning and level progression
        if self.enemy_hold:
            if len(self.enemies) == 0:
                self.enemy_hold = False
        else:
            if self.timer < time() and len(self.level) != 0:
                self.timer = time() + self.s.spawn_speed

                line = self.level.pop(-1)
                position = 0
                for char in line:
                    position += 1
                    # If there is enemy calculate it's x position
                    if char != '-':
                        spacing = self.s.int_screen_width / self.s.level_width
                        pos_x = spacing * position - spacing / 2
                    # Stop spawning until all enemies are gone
                    if char == '_':
                        self.enemy_hold = True
                        break

                    if char == 'a':
                        self.enemies.add(asteroid.Asteroid(self.s, self.gfx, pos_x))

                    elif char == 's':
                        self.enemies.add(shifter.Shifter(self.s, self.gfx, pos_x))

                    elif char == '1':
                        self.enemies.add(boss.Boss1(self.s, self.gfx))

        # Enemy update
        self.enemies.update(dt, enemy_bullets, ship)

        # Get rid of enemies out of screen
        for sprite in self.enemies:
            if sprite.rect.top > self.s.int_screen_height:
                self.enemies.remove(sprite)

    def draw(self):
        self.enemies.draw(self.int_screen)
