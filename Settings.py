import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile


# TODO MAKE SETTINGS PRETTY


class Settings(tk.Frame):

    def __init__(self, parent, controller, processor):
        tk.Frame.__init__(self, parent)

        frame = tk.Frame(self, width=800, height=520, bg='#1D1D1D')
        frame.pack_propagate(0)
        frame.pack()

        """
        COMMANDS FOR BUTTONS
        """

        # FILE BROWSER, launches file browser for user to select a background.
        def open_file():
            file = askopenfile(mode='r', filetypes=[('All Files', '*.*'),
                                                    ('Text files', '*.txt*'),
                                                    ('PNG Image', '*.png')])

            if file is not None:
                current_path = file.name
                extension = (os.path.splitext(current_path)[1])[1:]

                # If the background file is gif > save into new_gif folder to be processed > processGif()
                if extension == 'gif':
                    path = r'./new_gif/'
                    destination = path + os.path.basename(file.name)
                    shutil.copyfile(current_path, destination)
                    processor.processGif(os.path.basename(file.name), path)

                # If the background file is an image (jpeg, png) > save into backgrounds folder > processImage()
                else:
                    path = r'./backgrounds/'
                    destination = path + os.path.basename(file.name)
                    if not os.path.exists(destination):
                        shutil.copyfile(current_path, destination)
                    processor.processImage(os.path.basename(file.name), path)
                controller.hide_settings()

        # RESIZE GUI
        def resize(choice):
            size = choice
            controller.update_screensize(size)

            if not size == "FULL SCREEN":
                screensize_file = open("screensize.txt", "w+")
                screensize_file.truncate(0)
                screensize_file.write(size)
                screensize_file.close()

        """
        BUTTONS
        """
        background_Button = Button(frame, text="Change Background", command=lambda: open_file())
        background_Button.pack(pady=20)

        screenSize_Menu = StringVar()
        screenSize_Menu.set("Change Screen Resolution")

        sizes = [
            "800x520",
            "1024x768",
            "1280x1024",
            "1600x1200",
            "1920x1080",
            "FULL SCREEN"
        ]

        dropdownSizes = OptionMenu(frame, screenSize_Menu, *sizes, command=resize)
        dropdownSizes.pack()
