# !/usr/bin/env python
import Tkinter as tk
import tkMessageBox
import pygame
from functools import partial
from json import loads, dumps


class GamepadConfig():
    """ Window that let's you assing game pad buttons to actions """

    def __init__(self, master=tk.Tk):
        self.controls = {}
        self.root = master
        self.root.grid()
        self.root.title('Space War 2027')

        # Init pygame and first joystick
        pygame.init()
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION, pygame.JOYHATMOTION])
        if pygame.joystick.get_count() == 0:
            tkMessageBox.showwarning('Warning', 'No gamepad detected')
            self.cancel()
            return
        else:
            gamepad = pygame.joystick.Joystick(0)
            gamepad.init()

        # Load configuration
        self.load()

        # Create widgets
        self.controls_frame = tk.LabelFrame(self.root, text='Gamepad configuration')

        self.left_button = tk.Button(self.controls_frame, text="LEFT", command=partial(self.set_btn, 'left'), width=6)
        self.right_button = tk.Button(self.controls_frame, text="RIGHT", command=partial(self.set_btn, 'right'), width=6)
        self.up_button = tk.Button(self.controls_frame, text="UP", command=partial(self.set_btn, 'up'), width=6)
        self.down_button = tk.Button(self.controls_frame, text="DOWN", command=partial(self.set_btn, 'down'), width=6)
        self.action1_button = tk.Button(self.controls_frame, text="A", command=partial(self.set_btn, 'action1'), width=6)
        self.action2_button = tk.Button(self.controls_frame, text="B", command=partial(self.set_btn, 'action2'), width=6)
        self.cancel_button = tk.Button(self.controls_frame, text="PAUSE\nCANCEL", command=partial(self.set_btn, 'cancel'))

        self.ok_button = tk.Button(self.root, text="Save", command=self.save,  width=6)
        self.no_button = tk.Button(self.root, text="Cancel", command=self.cancel,  width=6)

        # Place widgets to window
        self.left_button.grid(row=2, column=0, padx=10)
        self.up_button.grid(row=1, column=1, pady=5)
        self.down_button.grid(row=3, column=1, pady=5)
        self.right_button.grid(row=2, column=2, padx=10)
        self.cancel_button.grid(row=2, column=3, padx=20)
        self.action1_button.grid(row=1, column=4, padx=10)
        self.action2_button.grid(row=3, column=4)

        self.controls_frame.grid(row=0, columnspan=2, pady=5, padx=5)
        self.ok_button.grid(row=1, column=0, pady=5)
        self.no_button.grid(row=1, column=1)

    def set_btn(self, btn):
        """ Handle gamepad events and save them to controls """
        set = False
        while not set:
            pygame.event.clear()
            event = pygame.event.wait()

            # Allow buttons only for actions
            if btn in ['action1', 'action2', 'cancel']:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.controls[btn] = [event.button]
                    set = True

            # Allow axis and hat only for movement
            if btn in ['up', 'down', 'left', 'right']:
                if event.type == pygame.JOYHATMOTION:
                    if event.value != (0,0):
                        self.controls[btn] = [event.hat, event.value]
                        set = True
                if event.type == pygame.JOYAXISMOTION:
                    if event.value > 0.5 or event.value < -0.5:
                        if int(event.value) != 0:
                            self.controls[btn] = [event.axis, int(event.value)]
                            set = True

    def cancel(self):
        """ Exit window """
        pygame.quit()
        self.root.destroy()

    def load(self):
        """ Load gamepad bindings from file """
        try:
            with open('gamepad.json', 'r') as file:
                self.controls = loads(file.read())
        except:
            print 'Can\'t load config'

    def save(self):
        """ Save gamepad bindings and exit """
        js_data = dumps(self.controls, indent=4, separators=(',', ': '))

        try:
            with open('gamepad.json', 'w') as file:
                file.write(js_data)
        except IOError:
            print 'Can\'t save config'

        pygame.quit()
        self.root.destroy()


if __name__ == "__main__":
    app = GamepadConfig()
    app.root.mainloop()
