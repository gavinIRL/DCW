from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Frame
from random import randrange
import tkinter.font as tkFont


class ChartWindow(Frame):

    def __init__(self, master=None, mainwindow=None, **kwargs):
        Frame.__init__(self, master)
        self.root = master
        self.mainwindow = mainwindow
        self.width = 400
        self.height = 601
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, 10, 410)
        self.root.geometry(alignstr)

        # Variables to hold data
        self.list_times = []
        self.list_prices = []
        if "currency" in kwargs:
            self.currency_shown = kwargs.get("currency")
        else:
            self.currency_shown = "BTCUSDT"
        if "prices" in kwargs:
            self.list_prices = kwargs.get("prices")
        else:
            for i in range(10):
                self.list_prices.append(randrange(80, 100))
        if "times" in kwargs:
            self.list_times = kwargs.get("times")
        else:
            for i in range(10):
                self.list_times.append(i)
        self.init()

    def update(self, i):
        self.list_prices[-1] = randrange(90, 100)
        self.line.set_ydata(self.list_prices)
        return self.line,

    def init(self):
        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=12, weight="bold")

        self.root.title("Analysis")
        self.pack(fill='both', expand=1)

        vert_position = 5

        self.combo_time = ttk.Combobox(
            root, textvariable=self.currency_shown)
        self.combo_time.place(x=1, y=vert_position, width=74, height=25)

        self.combo_indicator = ttk.Combobox(
            root, textvariable=self.currency_shown)
        self.combo_indicator.place(x=75, y=vert_position, width=74, height=25)

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = self.currency_shown
        self.lbl_title.place(x=150, y=vert_position, width=100, height=25)

        self.combo_currency = ttk.Combobox(
            root, textvariable=self.currency_shown)
        self.combo_currency.place(x=250, y=vert_position, width=149, height=25)

        vert_position += 30
        self.lbl_indicators = tk.Label(self.root)
        self.lbl_indicators["font"] = font_heading
        self.lbl_indicators["justify"] = "center"
        self.lbl_indicators[
            "text"] = "RSI(6)=12.2  |  RSI(14)=15.3  |  MA(50)=52100.12  |  HV(10) = 40"
        self.lbl_indicators.place(
            x=0, y=vert_position, width=self.width, height=20)

        vert_position += 25

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.list_times, self.list_prices)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(x=0, y=vert_position,
                                          width=self.width, height=300)

        self.ani = animation.FuncAnimation(
            self.fig, self.update, np.arange(1, 10), interval=250, blit=False)

        vert_position += 305
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self.root, pack_toolbar=False,)
        self.toolbar.update()
        self.toolbar.place(relx=0.52, y=vert_position, width=300,
                           height=30, anchor=tk.constants.CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    # root.geometry("1000x800")
    cw = ChartWindow(root)
    tk.mainloop()
