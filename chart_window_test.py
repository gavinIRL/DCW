from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Frame, Label, Entry, Button
from random import randrange


class ChartWindow(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.root = root
        self.master = master
        self.init()

    def update(self, i):
        self.list_prices[-1] = randrange(90, 100)
        self.line.set_ydata(self.list_prices)
        return self.line,

    def init(self):
        self.width = 400
        self.height = 401
        self.master.title("Analysis")
        self.pack(fill='both', expand=1)

        self.list_prices = []
        self.list_times = []
        for i in range(10):
            self.list_prices.append(randrange(80, 100))
            self.list_times.append(i)

        print(self.list_times)
        # print(self.list_prices)
        #tk.Label(self, text="SHM Simulation").grid(column=0, row=0)

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.list_times, self.list_prices)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(x=0, y=0, width=self.width, height=self.height-50)
        #self.canvas.get_tk_widget().grid(row=1, column=0)

        self.ani = animation.FuncAnimation(
            self.fig, self.update, np.arange(1, 10), interval=250, blit=False)
        #print("Got to here")


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    root.geometry("1000x800")
    cw = ChartWindow(root)
    tk.mainloop()
