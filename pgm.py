#!/usr/bin/env python

from gfx import *
from sfx import SFX
from settings import Settings
from game import Game
from menu import Menu
from hud import HUD
from status import GameStatus
#import profile


def run_game():
    """Init game and run game"""
    # init config
    s = Settings()

    # pre-init sound
    pygame.mixer.pre_init(44100, -16, 2, 2048)

    # init pygame and screen
    pygame.init()
    if s.fullscreen:
        screen = pygame.display.set_mode((s.screen_width, s.screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((s.screen_width, s.screen_height))

    pygame.display.set_caption('Space War 2027')

    # Internal screen
    int_screen = pygame.Surface((s.int_screen_width, s.int_screen_height))

    show_loading(screen, s)

    # Calculate internal scaling
    scale = s.screen_width / float(s.int_screen_width)
    s.int_scale_width = int(s.int_screen_width * scale)
    s.int_scale_height = int(s.int_screen_height * scale)

    # Init sound
    sfx = SFX()
    # Init graphics
    gfx = GFX(s)
    # Init game clock
    clock = pygame.time.Clock()
    # Status
    status = GameStatus()
    # Init menu
    menu = Menu(int_screen, s, gfx, sfx, status)
    # Init game itself
    game = Game(s, gfx, sfx, int_screen, status)

    hud = HUD(status, s, gfx, screen, clock)

    # Main loop
    while True:
        dt = clock.tick(60)     # time between frames, should alter speed of everything that is not based on real time

        if status.game_running:
            if game.update(dt): # If update is true level ended -> start new level
                game = Game(s, gfx, sfx, int_screen, status)
            game.draw()
            status.update()
        else:
            menu.update(game, dt)
            menu.draw()

        update_screen(s, screen, int_screen, hud)


def update_screen(s, screen, int_screen, hud):
    """Update images on the screen and flip to the new screen."""
    screen.fill((25,25,25))

    # Scale internal screen
    if s.scaling:
        int_screen = pygame.transform.scale(int_screen, (s.int_scale_width, s.int_scale_height))

    # And put it on screen
    rect = int_screen.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(int_screen, rect)

    # Draw HUD
    hud.draw()

    # Flip buffer
    pygame.display.flip()


def show_loading(screen, s):
    """Show loading screen, renders independently on rest of the game"""
    text = Text(screen, s.font_main, 16, (255, 255, 255))
    screen.fill((0,0,0))
    rect = screen.get_rect()
    text.write('now loading...', rect.centerx, rect.centery, (255,255,255), origin='center')
    pygame.display.flip()


#profile.run('run_game()')
run_game()