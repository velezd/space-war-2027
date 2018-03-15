import pygame
from utilities import singleton


@singleton
class Events():
    def __init__(self):
        # init event variables
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.fire1_pressed = False
        self.fire2_pressed = False
        self.cancel_pressed = False

        self.up_released = False
        self.down_released = False
        self.left_released = False
        self.right_released = False
        self.fire1_released = False
        self.fire2_released = False
        self.cancel_released = False

        self.key_pressed = False

    def get_events(self):
        # Reset event variables
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.fire1_pressed = False
        self.fire2_pressed = False
        self.cancel_pressed = False

        self.up_released = False
        self.down_released = False
        self.left_released = False
        self.right_released = False
        self.fire1_released = False
        self.fire2_released = False
        self.cancel_released = False

        self.key_pressed = False

        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                exit()

            # Keypress events
            elif event.type == pygame.KEYDOWN:
                self.key_pressed = True

                if event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                elif event.key == pygame.K_LEFT:
                    self.left_pressed = True
                elif event.key == pygame.K_UP:
                    self.up_pressed = True
                elif event.key == pygame.K_DOWN:
                    self.down_pressed = True
                elif event.key == pygame.K_SPACE:
                    self.fire1_pressed = True
                elif event.key == pygame.K_RETURN:
                    self.fire2_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    self.cancel_pressed = True
                elif event.key == pygame.K_BACKSPACE:
                    self.cancel_pressed = True

            # Keyrelease events
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.right_released = True
                elif event.key == pygame.K_LEFT:
                    self.left_released = True
                elif event.key == pygame.K_UP:
                    self.up_released = True
                elif event.key == pygame.K_DOWN:
                    self.down_released = True
                elif event.key == pygame.K_SPACE:
                    self.fire1_released = True
                elif event.key == pygame.K_RETURN:
                    self.fire2_released = True
                elif event.key == pygame.K_ESCAPE:
                    self.cancel_released = True
                elif event.key == pygame.K_BACKSPACE:
                    self.cancel_released = True

