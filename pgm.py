from gfx import *
import game_functions as gf
from settings import Settings
from ship import Ship
from background import Background
from level import Level
from menu import Menu
from status import GameStatus
from pygame.sprite import Group
#import profile


def run_game():
    """Init game and run game"""
    # init config
    s = Settings()

    # init pygame and screen
    pygame.init()
    if s.fullscreen:
        s.screen_width = s.fscreen_width
        s.screen_height = s.fscreen_height
        screen = pygame.display.set_mode((s.screen_width, s.screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((s.screen_width, s.screen_height))

    pygame.display.set_caption('Game!')

    # Internal screen
    int_screen = pygame.Surface((s.int_screen_width, s.int_screen_height))

    # Init fonts
    text = Text(screen, s.font_main, 16, (255, 255, 255))
    gf.show_loading(screen, text)

    # Calculate internal scaling
    scale = s.screen_width / float(s.int_screen_width)
    s.int_scale_width = int(s.int_screen_width * scale)
    s.int_scale_height = int(s.int_screen_height * scale)

    # Init graphics
    gfx = GFX(s)

    # Status
    status = GameStatus()

    # Init ship and bullets
    ship = Ship(int_screen, s, gfx, status)
    bullets = Group()
    enemy_bullets = Group()

    # Init background
    background = Background(s, int_screen, gfx)

    # Init game clock
    clock = pygame.time.Clock()

    # Init menu
    menu = Menu(screen, int_screen, s, gfx)

    # Init level
    level = Level(s, gfx, int_screen)

    # Main loop
    while True:
        dt = clock.tick(60)     # time between frames, should alter speed of everything that is not based on real time

        if status.game_running:
            background.update(dt)

            level.update(dt, enemy_bullets)

            gf.check_events(s, ship, bullets, gfx, status)

            ship.update(dt)

            gf.update_bullets(bullets, enemy_bullets, s, dt)

            gf.check_collisions(ship, level.enemies, bullets, enemy_bullets)

            gf.update_screen(s, screen, int_screen, text, clock, background, level, ship, bullets, enemy_bullets)

            status.update()
        else:
            menu.update(status, dt)
            menu.draw()

#profile.run('run_game()')
run_game()