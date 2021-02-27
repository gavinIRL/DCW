import tkinter as tk
import tkinter.font as tkFont
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# Small bit of setup, need to use TkAgg instead of default
matplotlib.use("TkAgg")


class ChartWindow:
    def __init__(self, mainwindow, root):
        self.mainwindow = mainwindow
        self.root = root
        self.root.geometry("400x400+400+400")
        self.label = tk.Label(root, text=f"This is the chart window")
        self.label.pack()

        self.fig = Figure(figsize=(7, 7), dpi=115)
        self.fig.add_subplot(1, 1, 1).plot(
            [1, 2, 3, 4, 5], [100, 104, 121, 108, 132])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
