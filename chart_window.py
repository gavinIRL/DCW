import tkinter as tk
from tkinter.constants import CENTER
import tkinter.font as tkFont
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# Small bit of setup, need to use TkAgg instead of default
matplotlib.use("TkAgg")


class ChartWindow:
    def __init__(self, mainwindow, root, **kwargs):
        self.mainwindow = mainwindow
        self.root = root
        self.currency_list = kwargs.get("currency_list")
        self.currency_shown = tk.StringVar()
        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=12, weight="bold")

        width = 400
        height = 401
        alignstr = '%dx%d+%d+%d' % (width, height, 10, 410)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.root.title("Analysis")

        if "currency" in kwargs:
            self.currency_shown = kwargs.get("currency")
        else:
            self.currency_shown = "BTCUSDT"
        self.starting_candle = kwargs.get("candle")

        # self.label = tk.Label(
        #     root, text=f"This is the chart window for "+str(self.starting_currency))
        # self.label.pack()
        vert_position = 5

        self.combo_time = ttk.Combobox(
            root, textvariable=self.currency_shown)
        self.combo_time.place(x=1, y=vert_position, width=149, height=25)

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = self.currency_shown
        self.lbl_title.place(x=150, y=vert_position, width=100, height=25)

        self.combo_currency = ttk.Combobox(
            root, textvariable=self.currency_shown)
        self.combo_currency.place(x=250, y=vert_position, width=149, height=25)

        vert_position += 30
        self.lbl_net_worth = tk.Label(self.root)
        self.lbl_net_worth["font"] = font_heading
        self.lbl_net_worth["justify"] = "center"
        self.lbl_net_worth[
            "text"] = "RSI(6)=12.2  |  RSI(14)=15.3  |  MA(50)=52100.12  |  HV(10) = 40"
        self.lbl_net_worth.place(x=0, y=vert_position, width=width, height=20)

        self.fig = Figure(figsize=(7, 7), dpi=115)
        self.fig.add_subplot(1, 1, 1).plot(
            [1, 2, 3, 4, 5], [100, 104, 121, 108, 132])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self.root, pack_toolbar=False,)
        self.toolbar.update()

        vert_position += 25
        self.canvas.get_tk_widget().place(x=0, y=vert_position, width=width, height=300)
        vert_position += 305
        self.toolbar.place(relx=0.58, y=vert_position, width=300,
                           height=30, anchor=CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    cw = ChartWindow(None, root)
    root.mainloop()
