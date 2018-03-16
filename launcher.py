#!/usr/bin/env python
import Tkinter as tk
from json import loads, dumps
from sys import exit
from os import chdir
import subprocess
import gamepad_config


def get_resolutions(ratio):
    """ Returns recommended resolutions based on current aspect ratio"""
    ratio = round(ratio, 4)
    resolutions = {1.7786: ['1366x768'],
                   1.7778: ['1280x720', '1600x900', '1920x1080', '2560x1440', '3840x2160'],
                   2.3704: ['1280x720', '1600x900', '1920x1080', '2560x1440', '3840x2160'],
                   1.6: ['1280x800', '1440x900', '1680x1050', '1920x1200'],
                   1.25: ['1280x1024']}

    fourthree = ['640x480', '800x600', '1024x768']

    if ratio in resolutions.keys():
        fourthree += resolutions[ratio]

    return fourthree


class Application():
    """ Game launcher that lets you change configuration before starting the game """
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", exit)
        self.root.grid()
        self.root.title('Space War 2027')

        # Init old/default values
        self.width_old = 640
        self.height_old = 480
        self.fullscreen_old = 0
        self.scaling_old = 1
        self.vol_effects_old = 1.0
        self.vol_music_old = 1.0

        # Init tk variables
        self.fullscreen = tk.IntVar()
        self.fullscreen.set(self.fullscreen_old)
        self.scaling = tk.IntVar()
        self.scaling.set(self.scaling_old)
        self.vol_effects = tk.DoubleVar()
        self.vol_effects.set(self.vol_effects_old)
        self.vol_music = tk.DoubleVar()
        self.vol_music.set(self.vol_music_old)

        # Load cinfiguration
        self.load()
        self.resolution_old = str(self.width_old) + 'x' + str(self.height_old)

        # Get recommended resolutions
        self.resolutions = get_resolutions(float(self.root.winfo_screenwidth()) / self.root.winfo_screenheight())

        # Create widgets
        self.logo = tk.PhotoImage(file='gfx/launcher.gif')
        self.label_logo = tk.Label(self.root, image=self.logo)
        self.frame_graphics = tk.LabelFrame(self.root, text='Graphics')
        self.frame_graphics.grid_columnconfigure(index=1, weight=1)
        self.frame_sound = tk.LabelFrame(self.root, text='Sound')
        self.frame_sound.grid_columnconfigure(index=1, weight=1)

        # Create widgets graphics
        label_resolution = tk.Label(self.frame_graphics, text='Resolution')
        label_fullscreen = tk.Label(self.frame_graphics, text='Fullscreen')
        label_scaling = tk.Label(self.frame_graphics, text='Scaling')
        self.check_fullscreen = tk.Checkbutton(self.frame_graphics, variable=self.fullscreen)
        self.check_scaling = tk.Checkbutton(self.frame_graphics, variable=self.scaling)
        v = tk.StringVar(self.root)
        self.spin_resolutions = tk.Spinbox(self.frame_graphics, values=self.resolutions, textvariable=v)
        v.set(self.resolution_old)

        # Create widgets sound
        label_vol_effects = tk.Label(self.frame_sound, text='Effects volume')
        label_vol_music = tk.Label(self.frame_sound, text='Music volume')
        self.scale_vol_effects = tk.Scale(self.frame_sound, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                                          showvalue=0, length=170, variable=self.vol_effects)
        self.scale_vol_music = tk.Scale(self.frame_sound, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                                        showvalue=0, length=170, variable=self.vol_music)

        # Create buttons
        self.gamepad_button = tk.Button(self.root, text="Gamepad configuration", command=self.show_gamepad)
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.stop)

        # Place widgets - Graphics frame
        label_resolution.grid(row=0,column=0)
        self.spin_resolutions.grid(row=0, column=1, sticky='E', pady=1)
        label_fullscreen.grid(row=1, column=0)
        self.check_fullscreen.grid(row=1, column=1, sticky='E', pady=1)
        label_scaling.grid(row=2, column=0)
        self.check_scaling.grid(row=2, column=1, sticky='E', pady=1)
        # place widgets - Sound frame
        label_vol_effects.grid(row=0, column=0)
        self.scale_vol_effects.grid(row=0, column=1, sticky='E', pady=1)
        label_vol_music.grid(row=1, column=0)
        self.scale_vol_music.grid(row=1, column=1, sticky='E', pady=1)
        # Place widgets - main Grid
        self.label_logo.grid(row=0, columnspan=2)
        self.frame_graphics.grid(row=1, columnspan=2, padx=5, sticky='WE')
        self.frame_sound.grid(row=2, columnspan=2, padx=5, pady=5, sticky='WE')
        self.gamepad_button.grid(row=3, columnspan=2, sticky='WE')
        self.start_button.grid(row=4, columnspan=2, sticky='WE')
        self.quit_button.grid(row=5, columnspan=2, sticky='WE')

    def show_gamepad(self):
        """ Show gamepad configuration window """
        window = tk.Toplevel(self.root)
        gamepad_config.GamepadConfig(window)

    def start(self):
        """ Destroy launcher but continue with start of game """
        self.save()
        self.root.quit()
        self.root.destroy()

    def stop(self):
        """ Exit launcher """
        self.root.quit()
        exit()

    def load(self):
        """ Load Game settings from file """
        try:
            with open('settings.json', 'r') as file:
                data = loads(file.read())

            self.width_old = data['screen_width']
            self.height_old = data['screen_height']
            self.fullscreen_old = data['fullscreen']
            self.scaling_old = data['scaling']
            self.vol_effects_old = data['vol_effects']
            self.vol_music_old = data['vol_music']

            self.scaling.set(data['scaling'])
            self.fullscreen.set(data['fullscreen'])
            self.vol_effects.set(data['vol_effects'])
            self.vol_music.set(data['vol_music'])

        except:
            # if load fails create new settings file with default values
            print 'Can\'t load game settings'
            self.save()

    def save(self):
        """ Save Game config to file, if changed """
        res = self.spin_resolutions.get().split('x')
        fs = self.fullscreen.get()
        sc = self.scaling.get()
        ve = self.vol_effects.get()
        vm = self.vol_music.get()

        old = [self.width_old, self.height_old, self.fullscreen_old,
               self.scaling_old, self.vol_effects, self.vol_music]
        new = [res[0], res[1], fs, sc, ve, vm]

        # If any value changes save config
        for i in range(len(old)):
            if old[i] != new[i]:
                data = {'screen_width': res[0],
                        'screen_height': res[1],
                        'scaling': sc,
                        'fullscreen': fs,
                        'vol_effects': ve,
                        'vol_music': vm}

                js_data = dumps(data, indent=4, separators=(',', ': '))

                try:
                    with open('settings.json', 'w') as file:
                        file.write(js_data)
                except IOError:
                    print 'Can\'t save config'

                break


app = Application()
app.root.mainloop()

# Start game
chdir('src')
subprocess.call('python sw2027.py')