import os
import tkinter as tk
from tkinter import *


class ButtonMenu(tk.Frame):

    # full means word expanded, f stands for frame that is passed that button will switch to

    def __init__(self, parent, controller, screen_height, b1full, b2full, b3full, b4full, b1, b2, b3, b4, f1, f2, f3,
                 f4):
        tk.Frame.__init__(self, parent)

        # LEFT FRAME BUTTON MENU
        min_w = 50
        max_w = 90
        self.current_w = min_w
        self.expanded = False

        def expand():
            self.current_w += 5
            rep = frame.after(10, expand)
            frame.config(width=self.current_w)
            if self.current_w >= max_w:
                self.expanded = True
                frame.after_cancel(rep)
                fill()

        def contract():
            self.current_w -= 5
            rep = frame.after(10, contract)
            frame.config(width=self.current_w)
            if self.current_w <= min_w:
                self.expanded = False
                frame.after_cancel(rep)
                fill()

        def fill():
            if self.expanded:
                buttonL1.config(text=b1full, image='')
                buttonL2.config(text=b2full, image='')
                buttonL3.config(text=b3full, image='')
                buttonL4.config(text=b4full, image='')
                listButton.config(text="List", image='')
                settingsButton.config(text="Settings", image='')
            else:
                buttonL1.config(image=b1img)
                buttonL2.config(image=b2img)
                buttonL3.config(image=b3img)
                buttonL4.config(image=b4img)
                listButton.config(image=list_img)
                settingsButton.config(image=settings_img)

        self.update()
        frame = tk.Frame(self, bg="white", width=min_w, height=screen_height)
        frame.pack(side="left", fill="y")

        path = './menu_icons/'
        b1img = PhotoImage(file=os.path.join(path, b1)).subsample(2)
        b2img = PhotoImage(file=os.path.join(path, b2)).subsample(2)
        b3img = PhotoImage(file=os.path.join(path, b3)).subsample(2)
        b4img = PhotoImage(file=os.path.join(path, b4)).subsample(2)
        list_img = PhotoImage(file=os.path.join(path, 'list.png')).subsample(2)
        settings_img = PhotoImage(file=os.path.join(path, 'settings.png')).subsample(2)

        buttonL1 = tk.Button(frame, image=b1img, bg="white", fg="black", relief="flat",
                             command=lambda: controller.show_frame(f1))
        buttonL1.pack(side=tk.TOP, padx=2, pady=15)

        buttonL2 = tk.Button(frame, image=b2img, bg="white", fg="black", relief="flat",
                             command=lambda: controller.show_frame(f2))
        buttonL2.pack(side=tk.TOP, padx=2, pady=15)

        buttonL3 = tk.Button(frame, image=b3img, bg="white", fg="black", relief="flat",
                             command=lambda: controller.show_frame(f3))
        buttonL3.pack(side=tk.TOP, padx=2, pady=15)

        buttonL4 = tk.Button(frame, image=b4img, bg="white", fg="black", relief="flat",
                             command=lambda: controller.show_frame(f4))
        buttonL4.pack(side=tk.TOP, padx=2, pady=15)

        listButton = tk.Button(frame, image=list_img, bg="white", fg="black", relief="flat",
                               command=lambda: controller.toggle_list())
        listButton.pack(side=tk.BOTTOM, padx=2, pady=15)

        settingsButton = tk.Button(frame, image=settings_img, bg="white", fg="black", relief="flat",
                                   command=lambda: controller.toggle_settings())
        settingsButton.pack(side=tk.BOTTOM, padx=2, pady=15)

        frame.bind('<Enter>', lambda e: expand())
        frame.bind('<Leave>', lambda e: contract())

        frame.pack_propagate(0)
