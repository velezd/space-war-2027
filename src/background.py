from time import time
from random import randint
from pygame.sprite import Group
from effects import stars
from config import CFG


class Background():
    """Manage and draw level background"""
    def __init__(self, int_screen, image, type='flyby', use_stars=1, lenght=0):
        """
        Inits level background, background types:
        flyby - image flies by exactly once on random x position
        repeat - image continually flies by on random x position, with short random pauses in repeat
        scroll - image scrolls continually from top to bottom, with no spaces in between and no randomness

        :param int_screen: screen surface
        :param image: background image
        :param type: background type
        :param use_stars: show random stars flying by
        :param lenght: lenght of the level lines
        """
        self.background = image
        self.int_screen = int_screen
        self.back_rect = self.background.get_rect()
        self.use_stars = use_stars

        self.back_speed = 0.03

        # set background type / animation, image position based on type
        if type in ['flyby','repeat']:
            if type == 'repeat':
                self.type = 2
            else:
                self.type = 0
                # calculate speed for fly-by
                times = lenght * CFG().spawn_speed
                self.back_speed = (self.int_screen.get_rect().height + self.background.get_rect().height) / float(times)
            # random position on screen
            self.back_pos_y = 0.0
            self.back_rect.bottom = 0
            self.back_rect.centerx = randint(0, CFG().int_screen_width)

        elif type == 'scroll':
            self.type = 1
            # Background image starts by already filling the entire screen
            self.back_rect.bottom = CFG().int_screen_height
            self.back_pos_y = float(self.back_rect.bottom)
            # and is aligned to left
            self.back_rect.left = 0
            # Second rect is needed to draw to images on screen at once
            self.back_rect2 = self.back_rect.copy()
            self.back_rect2.bottom = self.back_rect.top
            self.back_pos2_y = float(self.back_rect2.bottom)

        # init stars if needed
        if self.use_stars:
            self.stars = Group()
            stars.generate_init_stars(self.stars, 20, self.int_screen, 180)
            self.gen_speed = 0.1

            self.stars_timer = time() + self.gen_speed

    def update(self, dt, pause):
        """ Background update """
        # Type flyby
        if self.type == 0:
            if not pause:
                self.back_pos_y += self.back_speed * (dt / 1000.0)
                self.back_rect.bottom = self.back_pos_y

        # Type scroll
        elif self.type == 1:
            # Move images
            self.back_pos_y += self.back_speed * dt
            self.back_pos2_y += self.back_speed * dt
            self.back_rect.bottom = self.back_pos_y
            self.back_rect2.bottom = self.back_pos2_y
            # If rect 1 bellow screen move rect to the top
            if self.back_rect.top > CFG().int_screen_height:
                self.back_rect.bottom = self.back_rect2.top
                self.back_pos_y = self.back_rect.bottom
            # If rect 2 bellow screen move rect to the top
            if self.back_rect2.top > CFG().int_screen_height:
                self.back_rect2.bottom = self.back_rect.top
                self.back_pos2_y = self.back_rect2.bottom

        # Type repeat
        elif self.type == 2:
            # If rect bellow set new random position on top
            if self.back_rect.top > CFG().int_scale_height:
                self.back_rect.centerx = randint(0, CFG().int_screen_width)
                self.back_pos_y = randint(0, CFG().int_screen_height / 2) * -1

            # move image
            self.back_pos_y += self.back_speed * dt
            self.back_rect.bottom = self.back_pos_y

        # Stars
        if self.use_stars:
            self.stars.update(dt)

            # Add stars
            if self.stars_timer < time():
                self.stars_timer = time() + self.gen_speed
                self.stars.add(stars.Star(self.int_screen, 180))

    def draw(self):
        """ Draw background """
        self.int_screen.fill((0, 0, 0))

        if self.back_rect.bottom > 0:
            self.int_screen.blit(self.background, self.back_rect)

        # In case of scroll drw image on second rect
        if self.type == 1:
            if self.back_rect2.bottom > 0:
                self.int_screen.blit(self.background, self.back_rect2)

        if self.use_stars:
            self.stars.draw(self.int_screen)