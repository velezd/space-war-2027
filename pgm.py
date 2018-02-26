#!/usr/bin/env python

from gfx import *
from settings import Settings
from game import Game
from menu import Menu
from status import GameStatus
#import profile


def run_game():
    """Init game and run game"""
    # init config
    s = Settings()

    # init pygame and screen
    pygame.init()
    if s.fullscreen:
        screen = pygame.display.set_mode((s.screen_width, s.screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((s.screen_width, s.screen_height))

    pygame.display.set_caption('Space War 2027')

    # Internal screen
    int_screen = pygame.Surface((s.int_screen_width, s.int_screen_height))

    # Init fonts
    text = Text(screen, s.font_main, 16, (255, 255, 255))
    show_loading(screen, text)

    # Calculate internal scaling
    scale = s.screen_width / float(s.int_screen_width)
    s.int_scale_width = int(s.int_screen_width * scale)
    s.int_scale_height = int(s.int_screen_height * scale)

    # Init graphics
    gfx = GFX(s)
    # Init game clock
    clock = pygame.time.Clock()
    # Init menu
    menu = Menu(int_screen, s, gfx)
    # Status
    status = GameStatus()
    # Init game itself
    game = Game(s, gfx, int_screen, status)

    # Main loop
    while True:
        dt = clock.tick(60)     # time between frames, should alter speed of everything that is not based on real time

        if status.game_running:
            game.update(dt)
            game.draw()
            status.update()
        else:
            menu.update(status, game, dt)
            menu.draw()

        update_screen(s, screen, int_screen, text, clock)


def update_screen(s, screen, int_screen, text, clock):
    """Update images on the screen and flip to the new screen."""
    screen.fill((25,25,25))

    # Scale internal screen
    if s.scaling:
        int_screen = pygame.transform.scale(int_screen, (s.int_scale_width, s.int_scale_height))

    # And put it on screen
    rect = int_screen.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(int_screen, rect)

    # Print fps
    text.write(str(int(clock.get_fps())), 5, 5)

    # Flip buffer
    pygame.display.flip()


def show_loading(screen, text):
    """Show loading screen, renders independently on rest of the game"""
    screen.fill((0,0,0))
    rect = screen.get_rect()
    text.write('now loading...', rect.centerx, rect.centery, (255,255,255), origin='center')
    pygame.display.flip()


#profile.run('run_game()')
run_game()