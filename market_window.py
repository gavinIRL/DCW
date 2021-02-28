import tkinter as tk
import tkinter.font as tkFont
from dcw_utils import DCWUtils
from chart_window import ChartWindow


class MarketWindow:
    def __init__(self, mainwindow, root, currencies=["BTC", "ETH", "IOTA"]):
        self.mainwindow = mainwindow
        self.root = root
        self.currencies = currencies

        # These variables are for storing the latest data
        # Used for opening chart window from scratch and also pushing updates
        self.candles = []

        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=20, weight="bold")

        width = 676
        height = 456
        alignstr = '%dx%d+%d+%d' % (width, height, 10, 10)
        self.root.geometry(alignstr)

        self.root.resizable(width=False, height=False)
        self.root.title("Settings")

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = "Market (Base = USD)"
        self.lbl_title.place(x=0, y=5, width=width, height=25)

        horz_distance = 95
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "Current"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%24hr"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%1wk"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%1hr"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%5min"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(6)"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(14)"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "High"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "Low"
        self.lbl_heading.place(x=horz_distance, y=35, width=55, height=20)

        self.labels_symbols = []
        self.labels_current = []
        self.labels_change24h = []
        self.labels_change1w = []
        self.labels_change1h = []
        self.labels_change5m = []
        self.labels_rsi6 = []
        self.labels_rsi14 = []
        self.labels_high = []
        self.labels_low = []
        self.btns_chart = []
        for i, currency in enumerate(self.currencies):
            vert_spacing = 40
            horz_distance = 2
            if len(self.currencies) > 10:
                vert_spacing = int(400/len(self.currencies))
            label_symbol = tk.Label(
                root, text=currency, justify="left", font=font_label)
            label_symbol.place(
                x=horz_distance, y=55+i*vert_spacing, width=92, height=vert_spacing)
            self.labels_symbols.append(label_symbol)

            horz_distance += 93
            label_current = tk.Label(
                root, text="1.2345678", justify="center", font=font_label)
            label_current.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_current.append(label_current)

            horz_distance += 60
            label_change24h = tk.Label(
                root, text="+100.76%", justify="center", font=font_label)
            label_change24h.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change24h.append(label_change24h)

            horz_distance += 60
            label_change1w = tk.Label(
                root, text="+500.76%", justify="center", font=font_label)
            label_change1w.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change1w.append(label_change1w)

            horz_distance += 60
            label_change1h = tk.Label(
                root, text="+600.76%", justify="center", font=font_label)
            label_change1h.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change1h.append(label_change1h)

            horz_distance += 60
            label_change5m = tk.Label(
                root, text="-300.76%", justify="center", font=font_label)
            label_change5m.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change5m.append(label_change5m)

            horz_distance += 60
            label_rsi6 = tk.Label(root, text="16.72",
                                  justify="center", font=font_label)
            label_rsi6.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_rsi6.append(label_rsi6)

            horz_distance += 60
            label_rsi14 = tk.Label(
                root, text="26.72", justify="center", font=font_label)
            label_rsi14.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_rsi14.append(label_rsi14)

            horz_distance += 60
            label_high = tk.Label(root, text="2.3456789",
                                  justify="center", font=font_label)
            label_high.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_high.append(label_high)

            horz_distance += 60
            label_low = tk.Label(root, text="0.1234567",
                                 justify="center", font=font_label)
            label_low.place(
                x=horz_distance, y=55+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_low.append(label_low)

            horz_distance += 60
            btn_chart = tk.Button(root, text="Chart",
                                  justify="center", font=font_label)
            btn_chart["command"] = lambda i=i: self.btn_chart_command(i)
            btn_chart.place(x=horz_distance, y=55+i*vert_spacing,
                            width=40, height=vert_spacing-2)
            self.btns_chart.append(btn_chart)
        # Then fill out the initial data
        self.startup()
        # And then start updating candles every 2 mins while the window is open
        if self.mainwindow:
            DCWUtils.update_candles(self.mainwindow, self.root)

    def btn_chart_command(self, index):
        # print(index)
        self.mainwindow.new_window(
            _class=ChartWindow, currency=self.currencies[index])
        # Open chart window for the given currency
        pass

    def startup(self):
        for currency in self.currencies:
            # First need to grab all the current prices and get that data started
            pass
        for i, currency in enumerate(self.currencies):
            # Then need to go through the currencylist and get the candles to start off
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    sw = MarketWindow(None, root, currencies=[
        "BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "XLMUSDT",
        "BCHUSDT", "DOGEUSDT", "XEMUSDT", "ATOMUSDT", "XMRUSDT", "BSVUSDT", "EOSUSDT"])
    root.mainloop()
