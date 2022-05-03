import tkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor


class Test(tk.Tk):

    # initialize container and create other windows
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        frame = Whiteboard(container, self, 800, 520)
        frame.pack()


class Whiteboard(tk.Frame):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self, parent, controller, width, height):
        tk.Frame.__init__(self, parent)

        self.width = width
        self.height = height

        self.root = tk.Frame(self, width=self.width, height=self.height)
        self.root.pack()

        # MENU BAR (BOTTOM)
        bar = tk.Frame(self.root)
        bar.pack(side="bottom", padx=(self.width / 20, self.width / 8), pady=15)

        # COLORING
        bg_color = "#b6b4ae"
        btn_color = "#c7c5c1"
        parent.configure(bg=bg_color)
        self.root.configure(bg=bg_color)
        bar.configure(bg=btn_color)

        font_size = int(self.width / 60)
        b_font = f"Verdana {font_size}"

        self.pen_button = tk.Button(bar, text='pen', command=self.use_pen, font=b_font, bg=btn_color, relief='ridge',
                                    highlightcolor='white')
        self.pen_button.grid(row=0, column=0, padx=15)

        self.brush_button = tk.Button(bar, text='brush', command=self.use_brush, font=b_font, bg=btn_color, relief='flat')
        self.brush_button.grid(row=0, column=1, padx=15)

        self.color_button = tk.Button(bar, text='color', command=self.choose_color, font=b_font, bg=btn_color, relief='flat')
        self.color_button.grid(row=0, column=2, padx=15)

        self.eraser_button = tk.Button(bar, text='eraser', command=self.use_eraser, font=b_font, bg=btn_color, relief='flat')
        self.eraser_button.grid(row=0, column=3, padx=15)

        self.clear_button = tk.Button(bar, text='clear', command=self.clear, font=b_font, bg=btn_color, relief='flat')
        self.clear_button.grid(row=0, column=4, padx=15)

        self.choose_size_button = tk.Scale(bar, from_=1, to=100, orient=HORIZONTAL, font=b_font, bg=btn_color, relief='flat',
                                           troughcolor='white')
        self.choose_size_button.grid(row=0, column=5, padx=15)

        # WHITEBOARD
        self.c = Canvas(self.root, bg='white', width=(3 * self.width / 4), height=(3 * self.height / 4), relief='ridge')
        self.c.pack(side="top", padx=(self.width / 20, self.width / 8))

        # MOUSE SETUP aka B1
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        color = askcolor(color=self.color)[1]
        if color != None:
            self.color = color
        else:
            return None

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def clear(self):
        self.c.delete('all')

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief='flat')
        some_button.config(relief='ridge')
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == "__main__":
    test = Test()
    test.mainloop()
