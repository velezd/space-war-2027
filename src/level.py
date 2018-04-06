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

        self.text = Text(int_screen, CFG().font_main, 16, (255, 255, 255))

        self.layout = level['layout']
        self.background = Background(self.int_screen, GFX().background[level['background']],
                                     type=level['background_type'],
                                     use_stars=level['stars'],
                                     lenght=len(self.layout))
        self.story = Story(level['prestory'], level['poststory'], self.int_screen)
        self.next_level = level['nextlevel']
        self.name = level['name']
        self.music = level['music']

    def update(self, dt, enemy_bullets, ship, status):
        """
        Updated level, background and enemies
        :param dt:
        :param enemy_bullets:
        :param ship:
        :return: True if the game should be running, False if not
        """
        if not SFX().is_music_playing():
            SFX().music_play(self.music)

        # If at the start of level show story
        if self.starting:
            if self.story.update('start'):
                return False
            # No more story - start level
            self.show_name = True
            self.timer = time() + 3
            self.starting = False
            self.enemy_hold = True

        # Show level name, hold enemies
        elif self.show_name:
            if self.timer > time():
                self.enemy_hold = True
            else:
                self.show_name = False

        # No more level + no more enemies
        if len(self.layout) == 0 and len(self.enemies) == 0:
            # Show end story
            if self.story.update('end'):
                return False

            # End level
            self.ending = True
            pygame.mixer.music.stop()
            return True

        # Background update
        self.background.update(dt, self.enemy_hold)

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
        if self.story.story_image is not None:
            self.story.draw()
            return False

        self.background.draw()
        self.enemies.draw(self.int_screen)

        if self.show_name:
            rect = self.int_screen.get_rect()
            self.text.write(self.name, rect.width/2, rect.height/2, origin='center')

        return True


class Story():
    """ Shows story before and after level """
    def __init__(self, start_story, end_story, screen):
        """
        Init Story

        :param start_story: list of dict containing image name, time in seconds, and text
        :param end_story: list of dict containing image name, time in seconds, and text
        :param screen: surface to show the story on
        """
        self.start_story = start_story
        self.end_story = end_story
        self.screen = screen
        self.font = Text(self.screen, CFG().font_main, 11, (255, 255, 255), True)

        self.story_image = None
        self.story_timer = 0
        self.story_text = ''

        rect = self.screen.get_rect()
        self.text_x = rect.width / 2
        self.text_y = rect.height - (rect.height / 16)

    def update(self, set='start'):
        """
        Goes trough the story list, keeps duration for showing the story and updates current image and text

        :param set: string start or end - which part of story to show
        :return: True if showing image, False if all images have been shown
        """
        # If it's time for next story
        if self.story_timer < time():
            self.story_image = None
            self.story_text = ''

            if set == 'start':
                story = self.start_story
            else:
                story = self.end_story

            if len(story):
                page = story.pop(0)
                # Set next story image, duration and text
                self.story_image = GFX().story[page['image']]
                self.story_timer = time() + page['time']
                if 'text' in page.keys():
                    self.story_text = page['text']
            else:
                return False
        else:
            # Allow skipping of story at the start of level
            if set == 'start':
                if Events().key_pressed:
                    self.story_timer = 0

        return True

    def draw(self):
        """ Draw current story image and text"""
        self.screen.blit(self.story_image, self.story_image.get_rect())

        if self.story_text != '':
            text = self.story_text.split('\n')
            # Set initial padding from bottom based on number of lines
            y = self.text_y - (16 * len(text))

            for line in text:
                self.font.write(line, self.text_x, y, origin='center')
                y += 16