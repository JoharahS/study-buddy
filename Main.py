import tkinter as tk
from time import strftime
from tkinter import *

import numpy as np
from PIL import ImageTk, Image

from ButtonMenu import ButtonMenu
from Calculator import Calculator
from Calendar import JCalendar
from GifProcessor import Processor
from List import List
from Settings import Settings
from Timer import Timer
from Whiteboard import Whiteboard

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

"""
WINDOW CONTAINER --> Main Window

Default dimensions: 800 x 520, but screen size is resizeable
The actual display is referred to as Screen; hence Home_Screen, Calendar_Screen, Whiteboard_Screen
-Initialize the interchangeable frame classes on top of each other (Screen)
-Includes methods necessary for toggling other windows: To Do List, Settings
"""


# TODO POMODORO TIMER

class GUIProject(tk.Tk):

    def __init__(self, extension, num_frames, path, screensize, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.resizable(False, False)
        self.title("Study Buddy")
        self.overrideredirect(True)
        self.overrideredirect(False)
        self.grid_propagate(0)

        x = screensize.index('x')
        width = int(screensize[:x])
        height = int(screensize[x + 1:])
        root_screensize = f"{width + 90}x{height}"
        self.geometry(root_screensize)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # SETUP SCREENS TO BE DISPLAYED
        self.frames = {}

        frame = Home_Screen(self.container, self, width, height, extension, num_frames, path)
        self.frames[Home_Screen] = frame
        frame.grid(row=0, column=0, stick="nsew")

        for F in (Calendar_Screen, Whiteboard_Screen, Calculator_Screen, Timer_Screen):
            frame = F(self.container, self, width, height)
            self.frames[F] = frame
            frame.grid(row=0, column=0, stick="nsew")

        self.show_frame(Home_Screen)

        # SETUP TO DO LIST

        self.listShown = 0
        self.listWindow = tk.Toplevel(self)
        todoList = List(self.listWindow, self)
        todoList.pack()
        self.listWindow.protocol("WM_DELETE_WINDOW", self.hide_list)
        self.listWindow.attributes('-topmost', 'true')
        self.hide_list()

        # SETUP SETTINGS

        self.settingsShown = 0
        self.settingsWindow = tk.Toplevel(self)
        self.settingsWindow.resizable(False, False)  # Not resizable
        processor = Processor(self.container, self)
        settings = Settings(self.settingsWindow, self, processor)
        settings.pack()
        self.settingsWindow.protocol("WM_DELETE_WINDOW", self.hide_settings)
        self.hide_settings()

        # BIND ESCAPE BUTTON TO MAKE APPLICATION WINDOWED
        def window(event):
            self.update_screensize("800x520")
            screensize_file = open(dir_path + "/screensize.txt", "w+")
            screensize_file.truncate(0)
            screensize_file.write("800x520")
            screensize_file.close()
            self.hide_settings()

        def end(event):
            print("terminating gui...")
            self.destroy()

        self.bind('<Delete>', end)
        self.bind('<Escape>', window)
        self.settingsWindow.bind('<Delete>', end)
        self.settingsWindow.bind('<Escape>', window)

    # MAIN DISPLAY CONFIGURATIONS

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def update_home_background(self, container, extension, frameCount, path):
        self.frames[Home_Screen].destroy()
        # Create a new Home Screen with selected background
        screensize_file = open(dir_path + "/screensize.txt", "r")
        screensize = screensize_file.readline()
        screensize_file.close()
        x = screensize.index('x')
        width = int(screensize[:x])
        height = int(screensize[x + 1:])

        frame = Home_Screen(container, self, width, height, extension, frameCount, path)
        self.frames[Home_Screen] = frame
        frame.grid(row=0, column=0, stick="nsew")

    def update_screensize(self, size):
        if size == "FULL SCREEN":
            self.fullscreen()
        else:
            self.attributes('-fullscreen', False)
            x = size.index('x')
            width = int(size[:x])
            height = int(size[x + 1:])
            print(f"{width}, {height}")

            self.container.configure(width=width + 90, height=height)
            self.frames[Home_Screen].resize(width, height)
            self.frames[Calendar_Screen].resize(width, height)
            self.frames[Whiteboard_Screen].resize(width, height)
            self.frames[Calculator_Screen].resize(width, height)
            self.frames[Timer_Screen].resize(width, height)

            dimension = f"{width + 90}x{height}"
            self.geometry(dimension)

    def fullscreen(self):
        self.attributes('-fullscreen', True)
        width = self.winfo_width()
        height = self.winfo_height()
        print(f"{width}, {height}")

        self.container.configure(width=width, height=height)
        self.frames[Home_Screen].resize(width - 90, height)
        self.frames[Calendar_Screen].resize(width - 90, height)
        self.frames[Whiteboard_Screen].resize(width - 90, height)
        self.frames[Calculator_Screen].resize(width - 90, height)
        self.frames[Timer_Screen].resize(width - 90, height)

    # TOGGLING WINDOWS (TO DO LIST)

    def show_list(self):
        if self.listShown == 0:
            self.listWindow.deiconify()
            self.listShown = 1

    def hide_list(self):
        self.listWindow.withdraw()
        self.listShown = 0

    def toggle_list(self):
        if self.listShown == 1:
            self.hide_list()
        else:
            self.show_list()

    # TOGGLING WINDOWS (SETTINGS)

    def show_settings(self):
        if self.settingsShown == 0:
            self.settingsWindow.deiconify()
            self.settingsShown = 1

    def hide_settings(self):
        self.settingsWindow.withdraw()
        self.settingsShown = 0

    def toggle_settings(self):
        if self.settingsShown == 1:
            self.hide_settings()
        else:
            self.show_settings()


"""
HOME SCREEN
Opening screen, if users aren't using any of the functional screens they can stay on this screen for the 'aesthetic'.
Simple display with time. Users are able to change their home background in settings.
"""


class Home_Screen(tk.Frame):

    def __init__(self, parent, controller, screen_width, screen_height, extension, frameCount, path):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.extension = extension
        self.frameCount = frameCount
        self.path = path

        self.right_frame(screen_width, screen_height)
        self.left_frame(controller, screen_width, screen_height)

    # RIGHT FRAME (SCREEN)
    def right_frame(self, screen_width, screen_height):
        self.rightFrame = tk.Frame(self, width=screen_width, height=screen_height, bg="black")
        self.rightFrame.configure(width=screen_width, height=screen_height)
        self.rightFrame.pack(side="right")
        self.rightFrame.pack_propagate(0)

        # GIF Background
        def loadGif():
            print("loading gif...")
            frames = [PhotoImage(file=self.path, format='gif -index %i' % i) for i in range(self.frameCount)]
            xMultiplier = screen_width / frames[0].width()
            yMultiplier = screen_height / frames[0].height()

            if xMultiplier > yMultiplier:
                multiplier = xMultiplier
            else:
                multiplier = yMultiplier

            def update(index):
                # If multiplier > 1, gif is too small --> zoom in
                # If multiplier < 1, gif is too big --> zoom out (subsample)
                if multiplier >= 1:
                    m = round(multiplier + 0.5)
                    frame = frames[index].zoom(m)
                else:
                    m = np.reciprocal(multiplier)
                    m = round(multiplier + 0.5)
                    frame = frames[index].subsample(m)
                index += 1
                if index == self.frameCount:
                    index = 0
                background.image = frame
                background.configure(image=frame)

                def time():
                    string = strftime(' %H : %M  %p ')
                    clock.config(text=string)

                # Time Display
                w = 490
                h = 116
                xplacement = int((screen_width - w) / 2)
                yplacement = int((screen_height - h) / 2)
                clock_frame = tk.Frame(background, width=w, height=h)
                clock_frame.pack_propagate(0)
                clock_frame.place(relx=1.0, rely=1.0, x=-xplacement, y=-yplacement, anchor="se")
                clock = tk.Label(clock_frame, fg="white", bg='black', font=('Ebrima', 60, 'bold'))
                clock.pack(fill=BOTH, expand=1)
                time()

                self.rightFrame.after(60, update, index)

            # PLACE BACKGROUND WIDGET INTO RIGHT FRAME OF HOME FRAME
            background = tk.Label(self.rightFrame)
            background.pack(expand='true')

            self.rightFrame.after(0, update, 0)

        # Image background
        def loadImg():
            print("loading img...")

            def time():
                string = strftime(' %H : %M %p ')
                clock.config(text=string)
                clock.after(1000, time)

            background = tk.Label(self.rightFrame, bg='black')
            self_path = str(self.path)
            img = Image.open(str(dir_path) + self_path[self_path.index("/"):])
            rimg = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            bgImg = ImageTk.PhotoImage(rimg)
            background.image = bgImg
            background.configure(image=bgImg)
            background.pack()

            w = 490
            h = 116
            xplacement = int((screen_width - w) / 2)
            yplacement = int((screen_height - h) / 2)
            clock_frame = tk.Frame(background, width=w, height=h)
            clock_frame.pack_propagate(0)
            clock_frame.place(relx=1.0, rely=1.0, x=-xplacement, y=-yplacement, anchor="se")
            clock = tk.Label(clock_frame, fg="white", bg='black', font=('Ebrima', 60, 'bold'))
            clock.pack(fill=BOTH, expand=1)
            time()

        if self.extension == "gif":
            loadGif()
        else:
            loadImg()

    # LEFT FRAME (MENU)
    def left_frame(self, controller, screen_width, screen_height):
        self.leftFrame = tk.Frame(self, width=90, height=screen_height, bg="white")
        self.leftFrame.pack(side="left")
        self.leftFrame.pack_propagate(0)

        menu = ButtonMenu(self.leftFrame, controller, screen_height, " Calendar ", " Whiteboard ", " Calculator",
                          " Timer ", 'calendar.png', 'pen.png',
                          'calculator.png', 'timer.png', Calendar_Screen, Whiteboard_Screen, Calculator_Screen,
                          Timer_Screen)
        menu.pack(side="left", padx=10)

    def resize(self, nWidth, nHeight):
        self.rightFrame.destroy()
        self.leftFrame.destroy()
        self.configure(width=nWidth + 90, height=nHeight)
        self.right_frame(nWidth, nHeight)
        self.left_frame(self.controller, nWidth, nHeight)


"""
CALENDAR SCREEN
"""


# TODO CALENDAR


class Calendar_Screen(tk.Frame):

    def __init__(self, parent, controller, screen_width, screen_height):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rightFrame = tk.Frame(self, width=screen_width, height=screen_height)
        self.cal = JCalendar(self.rightFrame, screen_width, screen_height, self.controller)
        self.leftFrame = tk.Frame(self, width=90, height=screen_height, bg="white")
        self.menu = ButtonMenu(self.leftFrame, self.controller, screen_height, " Home ", " Whiteboard ", " Calculator ",
                               " Timer ", 'home.png', 'pen.png', 'calculator.png', 'timer.png', Home_Screen,
                               Whiteboard_Screen, Calculator_Screen, Timer_Screen)

        self.rightFrame.pack(side="right", fill="both", expand=True)
        self.rightFrame.pack_propagate(0)
        self.cal.pack()
        self.leftFrame.pack(side="left")
        self.leftFrame.pack_propagate(0)
        self.menu.pack(side="left", padx=10)

    def resize(self, nWidth, nHeight):
        self.rightFrame.destroy()
        self.rightFrame = tk.Frame(self, width=nWidth, height=nHeight)
        self.cal = JCalendar(self.rightFrame, nWidth, nHeight, self.controller)
        self.rightFrame.pack(side="right", fill="both", expand=True)
        self.rightFrame.pack_propagate(0)
        self.cal.pack()

        self.leftFrame.configure(height=nHeight)
        self.menu.destroy()
        self.menu = ButtonMenu(self.leftFrame, self.controller, nHeight, " Home ", " Whiteboard ", " Calculator ",
                               " Timer ", 'home.png', 'pen.png', 'calculator.png', 'timer.png', Home_Screen,
                               Whiteboard_Screen, Calculator_Screen, Timer_Screen)
        self.menu.pack(side="left", padx=10)


"""
WHITEBOARD SCREEN
Functional screen that allows users to draw and sketch, useful for if they need to draft something or visualize work.
"""


# TODO add clear button
# TODO make aesthetic

class Whiteboard_Screen(tk.Frame):

    def __init__(self, parent, controller, screen_width, screen_height):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rightFrame = Whiteboard(self, controller, screen_width, screen_height)
        self.leftFrame = tk.Frame(self, width=90, height=screen_height, bg="white")
        self.menu = ButtonMenu(self.leftFrame, self.controller, screen_height, " Home ", " Calendar ", " Calculator ",
                               " Timer ", 'home.png', 'calendar.png', 'calculator.png', 'timer.png', Home_Screen,
                               Calendar_Screen, Calculator_Screen, Timer_Screen)

        self.rightFrame.pack(side="right")
        self.leftFrame.pack(side="left")
        self.leftFrame.pack_propagate(0)
        self.menu.pack(side="left", padx=10)

    def resize(self, nWidth, nHeight):
        self.rightFrame.destroy()
        self.rightFrame = Whiteboard(self, self.controller, nWidth, nHeight)
        self.rightFrame.pack(side="right")

        self.leftFrame.configure(height=nHeight)
        self.menu.destroy()
        self.menu = ButtonMenu(self.leftFrame, self.controller, nHeight, " Home ", " Whiteboard ", " Calculator ",
                               " Timer ", 'home.png', 'pen.png', 'calculator.png', 'timer.png', Home_Screen,
                               Whiteboard_Screen, Calculator_Screen, Timer_Screen)
        self.menu.pack(side="left", padx=10)


"""
CALCULATOR
Basic scientific calendar. Borrowed code from internet...
"""


# TODO ALTER FORMATTING AND APPEARANCE


class Calculator_Screen(tk.Frame):

    def __init__(self, parent, controller, screen_width, screen_height):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.calc = Calculator(self, controller)
        self.leftFrame = tk.Frame(self, width=90, height=screen_height, bg="white")
        self.menu = ButtonMenu(self.leftFrame, self.controller, screen_height, " Home ", " Calendar ", " Whiteboard ",
                               " Timer ", 'home.png', 'calendar.png', 'pen.png', 'timer.png', Home_Screen,
                               Calendar_Screen, Whiteboard_Screen, Timer_Screen)

        self.calc.pack(side="right", padx=(screen_width / 10, screen_width / 3.5))
        self.leftFrame.pack(side="left")
        self.leftFrame.pack_propagate(0)
        self.menu.pack(side="left", padx=10)

    def resize(self, nWidth, nHeight):
        self.calc.destroy()
        self.calc = Calculator(self, self.controller)
        self.calc.pack(side="right", padx=(nWidth / 10, nWidth / 3.5))

        self.leftFrame.configure(height=nHeight)
        self.menu.destroy()
        self.menu = ButtonMenu(self.leftFrame, self.controller, nHeight, " Home ", " Calendar ", " Whiteboard ",
                               " Timer ", 'home.png', 'calendar.png', 'pen.png', 'timer.png', Home_Screen,
                               Calendar_Screen, Whiteboard_Screen, Timer_Screen)
        self.menu.pack(side="left", padx=10)


"""
TIMER SCREEN
Mainly pomodoro timer but can set other times as well.
"""


class Timer_Screen(tk.Frame):

    def __init__(self, parent, controller, screen_width, screen_height):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rightFrame = Timer(self, screen_width, screen_height)
        self.leftFrame = tk.Frame(self, width=90, height=screen_height, bg="white")
        self.menu = ButtonMenu(self.leftFrame, self.controller, screen_height, " Home ", " Calendar ", " Calculator ",
                               " Whiteboard ", 'home.png', 'calendar.png', 'calculator.png', 'pen.png', Home_Screen,
                               Calendar_Screen, Calculator_Screen, Whiteboard_Screen)

        self.rightFrame.pack(side="right")
        self.leftFrame.pack(side="left")
        self.leftFrame.pack_propagate(0)
        self.menu.pack(side="left", padx=10)

    def resize(self, nWidth, nHeight):
        self.rightFrame.destroy()
        self.rightFrame = Timer(self, nWidth, nHeight)
        self.rightFrame.pack(side="right")

        self.leftFrame.configure(height=nHeight)
        self.menu.destroy()
        self.menu = ButtonMenu(self.leftFrame, self.controller, nHeight, " Home ", " Calendar ", " Calculator ",
                               " Whiteboard ", 'home.png', 'calendar.png', 'calculator.png', 'pen.png', Home_Screen,
                               Calendar_Screen,
                               Calculator_Screen, Whiteboard_Screen)
        self.menu.pack(side="left", padx=10)


if __name__ == "__main__":
    homeBackground_file = open(dir_path + "/homeBackground.txt", "r")
    extension = homeBackground_file.readline()
    extension = extension.strip()
    path = homeBackground_file.readline()
    path = path.strip()
    frameCount = int(homeBackground_file.readline())
    homeBackground_file.close()

    screensize_file = open(dir_path + "/screensize.txt", "r")
    ss = screensize_file.readline()
    screensize_file.close()

    app = GUIProject(extension, frameCount, path, ss)
    app.mainloop()
