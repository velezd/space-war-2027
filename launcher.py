#!/usr/bin/env python
import Tkinter as tk
from json import loads, dumps
from sys import exit
from os import chdir
import subprocess


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
        self.root.grid()
        self.root.title('Space War 2027')

        self.width_old = 0
        self.height_old = 0
        self.fullscreen_old = 0
        self.scaling_old = 0
        self.fullscreen = tk.IntVar()
        self.scaling = tk.IntVar()

        # Load cinfiguration
        self.load()
        self.resolution_old = str(self.width_old) + 'x' + str(self.height_old)

        # Get recommended resolutions
        self.resolutions = get_resolutions(float(self.root.winfo_screenwidth()) / self.root.winfo_screenheight())

        # Create widgets
        self.logo = tk.PhotoImage(file='gfx/launcher.gif')
        self.label_logo = tk.Label(self.root, image=self.logo)
        self.label_logo.grid(columnspan=2)

        label_resolution = tk.Label(self.root, text='Resolution')
        label_fullscreen = tk.Label(self.root, text='Fullscreen')
        label_scaling = tk.Label(self.root, text='Scaling')

        self.check_fullscreen = tk.Checkbutton(self.root, variable=self.fullscreen)
        self.check_scaling = tk.Checkbutton(self.root, variable=self.scaling)
        v = tk.StringVar(self.root)
        self.spin_resolutions = tk.Spinbox(self.root, values=self.resolutions, textvariable=v)
        v.set(self.resolution_old)

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.stop)

        # Place widget to window
        label_resolution.grid(row=4,column=0, pady=3)
        self.spin_resolutions.grid(row=4, column=1, pady=3)
        label_fullscreen.grid(row=5, column=0, pady=3)
        self.check_fullscreen.grid(row=5, column=1, pady=3)
        label_scaling.grid(row=6, column=0, pady=3)
        self.check_scaling.grid(row=6, column=1, pady=3)

        self.start_button.grid(row=7, columnspan=2, sticky='WE')
        self.quit_button.grid(row=8, columnspan=2, sticky='WE')

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

            self.scaling.set(data['scaling'])
            self.fullscreen.set(data['fullscreen'])

        except IOError:
            print 'Can\'t load game settings'

    def save(self):
        """ Save Game config to file, if changed """
        fs = self.fullscreen.get()
        sc = self.scaling.get()
        res = self.spin_resolutions.get().split('x')

        if res[0] != self.width_old or res[1] != self.height_old or fs != self.fullscreen_old or sc != self.scaling_old:
            data = {'screen_width': res[0],
                    'screen_height': res[1],
                    'scaling': sc,
                    'fullscreen': fs}

            js_data = dumps(data, indent=4, separators=(',', ': '))

            try:
                with open('settings.json', 'w') as file:
                    file.write(js_data)
            except IOError:
                print 'Can\'t save config'

app = Application()
app.root.mainloop()

# Start game
chdir('src')
subprocess.call('./sw2027.py')