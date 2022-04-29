import tkinter as tk


class List(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame = tk.Frame(self, width=200, height=300, bg="white")
        frame.grid_propagate(0)
        frame.pack(side="right", padx=10, pady=10)

        # Index --> What Row
        index = 0
        frames = []
        entries = []
        checks = []

        def Next(index):

            if len(entries[index].get()) > 0:
                index = index + 1
                frames.append(tk.Frame(frame, bg="white"))
                frames[index].grid(row=index, column=0)

                checks.append(tk.Checkbutton(frames[index], bg="white", variable=index))
                checks[index].grid(row=0, column=0)
                entries.append(tk.Entry(frames[index], bg="white", fg="black", relief="flat"))
                entries[index].grid(row=0, column=1)
                entries[index].focus_set()

                entries[index].bind('<Return>', lambda e: Next(index))
                entries[index].bind('<BackSpace>', lambda e: Remove(index))

        def Remove(index):

            if index > 0 and len(entries[index].get()) == 0:
                frames[index].grid_forget()
                index = index - 1
                entries[index].focus_set()

        frames.append(tk.Frame(frame, bg="white"))
        frames[index].grid(row=index, column=0)

        entries.append(tk.Entry(frames[index], bg="white", fg="black", relief="flat"))
        entries[index].grid(row=0, column=1)
        checks.append(tk.Checkbutton(frames[index], bg="white", variable=index))
        checks[index].grid(row=0, column=0)

        entries[index].bind('<Return>', lambda e: Next(index))
        entries[index].bind('<BackSpace>', lambda e: Remove(index))
