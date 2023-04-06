import matplotlib
# matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)
style.use('ggplot')

fig, ax = plt.subplots()

xs =[0]
ys = [0]

def animate(i, xs, ys):
    y = np.random.randint(0,5)
    ys.append(y)
    xs.append(xs[-1] + 1)

    xs = xs[-20:]
    ys = ys[-20:]

    ax.clear()
    ax.plot(xs, ys)


class TestGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default='clienticon.ico')
        tk.Tk.wm_title(self, "My GUI client")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Main Page', font = LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Start Simulation",
                            command=lambda: controller.show_frame(GraphPage))
        button.pack()

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Graph', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Stop Simulation",
                             command = lambda:controller.show_frame(StartPage))
        button1.pack()

        canvas=FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


app = TestGUI()
ani = animation.FuncAnimation(fig, animate, fargs = (xs, ys), interval = 50, cache_frame_data=False)
app.mainloop()