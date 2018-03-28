import pygame
from time import time
from os import path
from json import loads
from pygame.sprite import Group
from enemies import asteroid, shifter, boss
from background import Background
from config import CFG
from gfx import GFX, Text
from sfx import SFX
from events import Events


class Level():
    def __init__(self, int_screen, filename=''):
        if not filename:
            filename = str(CFG().start_level)

        with open(path.join(CFG().path_levels, filename), 'r') as file:
            level = loads(file.read())

        self.int_screen = int_screen
        self.timer = 0
        self.enemies = Group()
        self.enemy_hold = False
        self.show_name = False

        self.starting = True
        self.ending = False
        self.story_image = None
        self.story_timer = 0

        self.text = Text(int_screen, CFG().font_main, 16, (255, 255, 255))

        self.layout = level['layout']
        self.background = Background(self.int_screen, GFX().background[level['background']])
        self.story_pre = level['prestory']
        self.story_post = level['poststory']
        self.next_level = level['nextlevel']
        self.name = level['name']
        self.music = level['music']

    def update(self, dt, enemy_bullets, ship, status):
        '''
        Updated level, background and enemies
        :param dt:
        :param enemy_bullets:
        :param ship:
        :return: True if the game should be running, False if not
        '''
        if not SFX().is_music_playing():
            SFX().music_play(self.music)

        # Things to do before level starts
        if self.starting:
            # Showing story - do nothing
            if self.story_timer > time():
                # Any keypress will skip story image
                if Events().key_pressed:
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
                if len(self.story_post) == 0 and self.story_timer < time():
                    self.ending = True
                    pygame.mixer.music.stop()
                    return True

        # Background update
        self.background.update(dt)

        # Enemy spawning and level progression
        if self.enemy_hold:
            if len(self.enemies) == 0:
                self.enemy_hold = False
        else:
            if self.timer < time() and len(self.layout) != 0:
                self.timer = time() + CFG().spawn_speed

                line = self.layout.pop(-1)
                position = 0
                for char in line:
                    position += 1
                    # If there is enemy calculate it's x position
                    if char != '-':
                        spacing = CFG().int_screen_width / CFG().level_width
                        pos_x = spacing * position - spacing / 2
                    # Stop spawning until all enemies are gone
                    if char == '_':
                        self.enemy_hold = True
                        break

                    if char == 'a':
                        self.enemies.add(asteroid.Asteroid(pos_x))

                    elif char == 's':
                        self.enemies.add(shifter.Shifter(pos_x))

                    elif char == '1':
                        self.enemies.add(boss.Boss1(status))

        # Enemy update
        self.enemies.update(dt, enemy_bullets, ship)

        # Get rid of enemies out of screen
        for sprite in self.enemies:
            if sprite.rect.top > CFG().int_screen_height:
                self.enemies.remove(sprite)

        return True

    def draw(self):
        # If showing story image, return False, nothing will render over it
        if self.story_image:
            self.draw_story()
            return False
        self.background.draw()
        self.enemies.draw(self.int_screen)
        if self.show_name:
            rect = self.int_screen.get_rect()
            self.text.write(self.name, rect.width/2, rect.height/2, color=None, origin='center')
        return True

    def draw_story(self):
        self.int_screen.blit(self.story_image, self.story_image.get_rect())

    def show_story(self, story):
        if len(story):
            page = story.pop(0)
            self.story_image = GFX().story[page['image']]
            self.story_timer = time() + page['time']