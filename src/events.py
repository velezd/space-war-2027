import pygame
from utilities import singleton
from json import loads
from config import CFG
from os import path


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

        # Gamepad
        self.gamepad = None
        self.gamepad_controls = {}

        if path.exists(CFG().path_gamepad):
            with open(CFG().path_gamepad, 'r') as file:
                self.gamepad_controls = loads(file.read())

        if pygame.joystick.get_count() != 0 and self.gamepad_controls:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()

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

            # Gamepad events
            if self.gamepad:
                # Button press
                if event.type == pygame.JOYBUTTONDOWN:
                    self.key_pressed = True
                    if event.button == self.gamepad_controls['action1'][0]:
                        self.fire1_pressed = True
                    elif event.button == self.gamepad_controls['action2'][0]:
                        self.fire2_pressed = True
                    elif event.button == self.gamepad_controls['cancel'][0]:
                        self.cancel_pressed = True
                # Button released
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == self.gamepad_controls['action1'][0]:
                        self.fire1_released = True
                    elif event.button == self.gamepad_controls['action2'][0]:
                        self.fire2_released = True
                    elif event.button == self.gamepad_controls['cancel'][0]:
                        self.cancel_released = True

                # Axis / hat movement
                if event.type == pygame.JOYAXISMOTION or pygame.JOYHATMOTION:
                    if 'axis' in dir(event):
                        axis = event.axis
                        value = int(event.value)
                    elif 'hat' in dir(event):
                        axis = event.hat
                        value = [event.value[0], event.value[1]]
                    else:
                        axis = None
                        value = None

                    if axis == self.gamepad_controls['up'][0]:
                        if value == self.gamepad_controls['up'][1]:
                            self.up_pressed = True
                        else:
                            self.up_released = True
                    if axis == self.gamepad_controls['down'][0]:
                        if value == self.gamepad_controls['down'][1]:
                            self.down_pressed = True
                        else:
                            self.down_released = True
                    if axis == self.gamepad_controls['left'][0]:
                        if value == self.gamepad_controls['left'][1]:
                            self.left_pressed = True
                        else:
                            self.left_released = True
                    if axis == self.gamepad_controls['right'][0]:
                        if value == self.gamepad_controls['right'][1]:
                            self.right_pressed = True
                        else:
                            self.right_released = True

