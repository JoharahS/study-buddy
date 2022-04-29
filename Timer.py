import time
import tkinter as tk
from tkinter import *


class Test(tk.Tk):

    # initialize container and create other windows
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("800x520")

        container = tk.Frame(self, width=800, height=520)
        container.pack(side="top", fill="both", expand=True)
        container.pack_propagate(0)

        frame = Timer(container, 800, 520)
        frame.pack()


class Timer(tk.Frame):

    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent)

        multiplier = int((width / 200) + 0.5)
        distance = .025 * multiplier
        font_size = 3 * multiplier
        times_font_size = 16 * multiplier
        times_font = f"Calibri {times_font_size}"
        timebutton_font = f"Calibri {font_size}"
        categorybutton_font = f"Calibri {font_size + 2}"
        widget_color = '#FAF9F6'
        hover_color = '#d9d7d2'

        root = tk.Frame(self, width=width, height=height, bg='#edebe6')
        root.pack()

        seconds = StringVar()
        tk.Entry(root, textvariable=seconds, width=5, justify=CENTER, font=times_font, relief=FLAT,
                 bg=widget_color).place(relx=.75, rely=.4, anchor=CENTER)
        seconds.set('00')

        minutes = StringVar()
        tk.Entry(root, textvariable=minutes, width=5, justify=CENTER, font=times_font, relief=FLAT,
                 bg=widget_color).place(relx=.5, rely=.4, anchor=CENTER)
        minutes.set('00')

        hours = StringVar()
        tk.Entry(root, textvariable=hours, width=5, justify=CENTER, font=times_font, relief=FLAT,
                 bg=widget_color).place(relx=.25, rely=.4, anchor=CENTER)
        hours.set('00')

        self.times = 0

        def countdowntimer():
            self.times = int(hours.get()) * 3600 + int(minutes.get()) * 60 + int(seconds.get())
            while self.times > -1:
                minute, second = (self.times // 60, self.times % 60)
                hour = 0
                if minute > 60:
                    hour, minute = (minute // 60, minute % 60)
                s = f"0{second}"
                s = s[-2:]
                m = f"0{minute}"
                m = m[-2:]
                h = f"0{hour}"
                h = h[-2:]
                seconds.set(s)
                minutes.set(m)
                hours.set(h)

                root.update()
                time.sleep(1)
                if self.times == 0:
                    seconds.set('00')
                    minutes.set('00')
                    hours.set('00')
                self.times -= 1

        def pomodoro():
            seconds.set('00')
            minutes.set('25')
            hours.set('00')

        def short():
            seconds.set('00')
            minutes.set('05')
            hours.set('00')

        def long():
            seconds.set('00')
            minutes.set('10')
            hours.set('00')

        def end():
            self.times = -1
            seconds.set('00')
            minutes.set('00')
            hours.set('00')

        def pause():
            seconds.set(int(seconds.get()) + 1)
            self.times = -1

        start_button = tk.Button(root, text='START', width=10, font=timebutton_font, command=countdowntimer,
                                 bg=widget_color,
                                 relief=FLAT)
        start_button.place(relx=(.4 - distance), rely=(.5 + distance), anchor=CENTER)

        pause_button = tk.Button(root, text='PAUSE', width=10, font=timebutton_font, command=pause, bg=widget_color,
                                 relief=FLAT)
        pause_button.place(relx=.5, rely=(.5 + distance), anchor=CENTER)

        end_button = tk.Button(root, text='END', width=10, font=timebutton_font, command=end, bg=widget_color,
                               relief=FLAT)
        end_button.place(relx=(.6 + distance), rely=(.5 + distance), anchor=CENTER)

        short_break_button = tk.Button(root, text='SHORT BREAK', width=(4 * multiplier) - 1, font=categorybutton_font,
                                       command=short,
                                       bg=widget_color, relief=FLAT)
        short_break_button.place(relx=(.4 - distance), rely=(.65 + distance), anchor=CENTER)

        pomodoro_button = tk.Button(root, text='POMODORO', width=(4 * multiplier) - 1, font=categorybutton_font,
                                    command=pomodoro, bg=widget_color,
                                    relief=FLAT)
        pomodoro_button.place(relx=.5, rely=(.65 + distance), anchor=CENTER)

        long_break_button = tk.Button(root, text='LONG BREAK', width=(4 * multiplier) - 1, font=categorybutton_font,
                                      command=long,
                                      bg=widget_color, relief=FLAT)
        long_break_button.place(relx=(.6 + distance), rely=(.65 + distance), anchor=CENTER)


if __name__ == "__main__":
    test = Test()
    test.mainloop()
