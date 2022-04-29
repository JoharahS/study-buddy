import tkinter as tk

from tkcalendar import Calendar


class Test(tk.Tk):

    # initialize container and create other windows
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("800x520")

        container = tk.Frame(self, width=800, height=520)
        container.pack(side="top", fill="both", expand=True)
        container.pack_propagate(0)

        frame = JCalendar(container, 800, 520, self)
        frame.pack()


class JCalendar(tk.Frame):

    def __init__(self, parent, width, height, root):
        tk.Frame.__init__(self, parent)

        self.cal = Calendar(parent, selectmode='day', year=2022, month=4, day=20)
        self.cal.pack(fill="both", expand=True)

        self.top = tk.Toplevel(root)
        self.top.pack_propagate(0)
        self.top.withdraw()

    def event(self):
        self.top.deiconify()
        tk.Label(self.top, text="Event adder").pack()

        def select_date():
            date.config(text="Selected Date Is: " + self.cal.get_date())

        tk.Button(self.top, text="Get Date", command=select_date).pack()
        date = tk.Label(self.top, text="")
        date.pack(pady=20)


if __name__ == "__main__":
    test = Test()
    test.mainloop()
