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
        self.height = 401
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, 10, 410)
        self.root.resizable(width=False, height=False)
        self.root.geometry(alignstr)

        # Variables to hold data
        self.list_times = []
        self.list_prices = []

        # This is for testing
        self.test_mode = True
        if "currency" in kwargs:
            self.start_currency = kwargs.get("currency")
        else:
            self.start_currency = "BTCUSDT"
        if "prices" in kwargs:
            self.list_prices = kwargs.get("prices")
            self.test_mode = False
        else:
            for i in range(10):
                self.list_prices.append(randrange(80, 100))
        if "times" in kwargs:
            self.list_times = kwargs.get("times")
        else:
            for i in range(len(self.list_prices)):
                self.list_times.append(i)
        if not self.mainwindow:
            self.currency_list = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT"]
        else:
            self.currency_list = self.mainwindow.market_currency_list
        self.init()

    def update(self, i):
        if self.test_mode:
            self.list_prices[-1] = randrange(90, 100)
        self.line.set_ydata(self.list_prices)
        return self.line,

    def change_box_time(self, eventObject):
        print(self.time_shown.get())

    def change_box_indicator(self, eventObject):
        print(self.indicator_shown.get())

    def change_box_currency(self, eventObject):
        self.lbl_title["text"] = self.currency_shown.get()
        print(self.currency_shown.get())

    def init(self):
        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=12, weight="bold")

        self.root.title("Analysis")
        self.pack(fill='both', expand=1)

        vert_position = 5

        self.time_shown = tk.StringVar()
        self.combo_time = ttk.Combobox(
            self.root, textvariable=self.time_shown, state="readonly")
        self.combo_time.place(x=1, y=vert_position, width=74, height=25)
        self.combo_time["values"] = (
            "1min", "5min", "10min", "15min", "30min", "1hr", "3hr", "6hr", "12hr", "1day")
        self.combo_time.current(1)
        self.combo_time.bind("<<ComboboxSelected>>", self.change_box_time)

        self.indicator_shown = tk.StringVar()
        self.combo_indicator = ttk.Combobox(
            self.root, textvariable=self.indicator_shown, state="readonly")
        self.combo_indicator.place(x=75, y=vert_position, width=74, height=25)
        self.combo_indicator["values"] = (
            "RSI(6)", "RSI(14)", "MA(50)", "HV(10)")
        self.combo_indicator.current(0)
        self.combo_indicator.bind(
            "<<ComboboxSelected>>", self.change_box_indicator)

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = self.start_currency
        self.lbl_title.place(x=150, y=vert_position, width=100, height=25)

        self.currency_shown = tk.StringVar()
        self.combo_currency = ttk.Combobox(
            self.root, textvariable=self.currency_shown, values=self.currency_list, state="readonly")
        self.combo_currency.place(x=250, y=vert_position, width=149, height=25)
        self.combo_currency.current(
            self.currency_list.index(self.start_currency))
        self.combo_currency.bind(
            "<<ComboboxSelected>>", self.change_box_currency)

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
        self.canvas.get_tk_widget().place(x=10, y=vert_position,
                                          width=self.width, height=300)

        self.ani = animation.FuncAnimation(
            self.fig, self.update, np.arange(1, 10), interval=250, blit=False)

        vert_position += 305
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self.root, pack_toolbar=False,)
        self.toolbar.update()
        self.toolbar.place(relx=0.58, y=vert_position, width=300,
                           height=30, anchor=tk.constants.CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    cw = ChartWindow(root)
    tk.mainloop()
