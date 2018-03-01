from time import time
from pygame.sprite import Group, Sprite
from json import loads
from enemies import asteroid, shifter, boss
from background import Background
from gfx import Text
import pygame


class Level():
    def __init__(self, s, gfx, int_screen, filename=''):
        if not filename:
            filename = str(s.start_level)

        with open('levels/' + filename, 'r') as file:
            level = loads(file.read())

        self.s = s
        self.gfx = gfx
        self.int_screen = int_screen
        self.timer = 0
        self.enemies = Group()
        self.enemy_hold = False
        self.show_name = False

        self.starting = True
        self.ending = False
        self.story_image = None
        self.story_timer = 0

        self.text = Text(int_screen, s.font_main, 16, (255, 255, 255))

        self.layout = level['layout']
        self.background = Background(self.s, self.int_screen, self.gfx.background[level['background']])
        self.story_pre = level['prestory']
        self.story_post = level['poststory']
        self.next_level = level['nextlevel']
        self.name = level['name']

    def update(self, dt, enemy_bullets, ship):
        '''
        Updated level, background and enemies
        :param dt:
        :param enemy_bullets:
        :param ship:
        :return: True if the game should be running, False if not
        '''

        # Things to do before level starts
        if self.starting:
            # Showing story - do nothing
            if self.story_timer > time():
                # Any keypress will skip story image
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.story_timer = 0
                return False
            else:
                self.story_image = None

            # Show next story image
            if len(self.story_pre) != 0:
                self.show_story(self.story_pre)
                return False
            # No more story images - start level
            self.show_name = True
            self.story_timer = time() + 3
            self.starting = False
            self.enemy_hold = True

        # Show level name, hold enemies
        elif self.show_name:
            if self.story_timer > time():
                self.enemy_hold = True
            else:
                self.show_name = False

        # No more level + no more enemies
        if len(self.layout) == 0 and len(self.enemies) == 0:
            if self.story_timer > time():
                return False
            else:
                # Show story
                self.show_story(self.story_post)
                # No more story - end game
                if len(self.story_post) == 0:
                    self.ending = True
                    return True

        # Background update
        self.background.update(dt)

        # Enemy spawning and level progression
        if self.enemy_hold:
            if len(self.enemies) == 0:
                self.enemy_hold = False
        else:
            if self.timer < time() and len(self.layout) != 0:
                self.timer = time() + self.s.spawn_speed

                line = self.layout.pop(-1)
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

        return True

    def draw(self):
        # If showing story image, return False, nothing will render over it
        if self.story_image:
            self.int_screen.blit(self.story_image, self.story_image.get_rect())
            return False

        self.background.draw()
        self.enemies.draw(self.int_screen)
        if self.show_name:
            rect = self.int_screen.get_rect()
            self.text.write(self.name, rect.width/2, rect.height/2, color=None, origin='center')
        return True

    def show_story(self, story):
        if len(story):
            page = story.pop(0)
            self.story_image = self.gfx.story[page['image']]
            self.story_timer = time() + page['time']