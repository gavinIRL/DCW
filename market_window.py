import tkinter as tk
import tkinter.font as tkFont


class MarketWindow:
    def __init__(self, mainwindow, root, currencies=["BTC", "ETH", "IOTA"]):
        self.mainwindow = mainwindow
        self.root = root
        self.currencies = currencies
        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=20, weight="bold")

        width = 616
        height = 456
        width_screen = self.root.winfo_screenwidth()
        alignstr = '%dx%d+%d+%d' % (width, height, 50, 50)
        self.root.geometry(alignstr)

        self.root.resizable(width=False, height=False)
        self.root.title("Settings")

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = "Market (Base = USD)"
        self.lbl_title.place(x=0, y=5, width=width, height=25)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "Current"
        self.lbl_heading.place(x=35, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%24hr"
        self.lbl_heading.place(x=95, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%1wk"
        self.lbl_heading.place(x=155, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%1hr"
        self.lbl_heading.place(x=215, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "%5min"
        self.lbl_heading.place(x=275, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(6)"
        self.lbl_heading.place(x=335, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(14)"
        self.lbl_heading.place(x=395, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "High"
        self.lbl_heading.place(x=455, y=35, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "Low"
        self.lbl_heading.place(x=515, y=35, width=55, height=20)

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
            spacing = 40
            if len(self.currencies) > 10:
                spacing = int(400/len(self.currencies))
            label_symbol = tk.Label(
                root, text=currency, justify="left", font=font_label)
            label_symbol.place(
                x=2, y=55+i*spacing, width=32, height=spacing)
            self.labels_symbols.append(label_symbol)

            label_current = tk.Label(
                root, text="1.2345678", justify="center", font=font_label)
            label_current.place(
                x=35, y=55+i*spacing, width=55, height=spacing)
            self.labels_current.append(label_current)

            label_change24h = tk.Label(
                root, text="+100.76%", justify="center", font=font_label)
            label_change24h.place(
                x=95, y=55+i*spacing, width=55, height=spacing)
            self.labels_change24h.append(label_change24h)

            label_change1w = tk.Label(
                root, text="+500.76%", justify="center", font=font_label)
            label_change1w.place(
                x=155, y=55+i*spacing, width=55, height=spacing)
            self.labels_change1w.append(label_change1w)

            label_change1h = tk.Label(
                root, text="+600.76%", justify="center", font=font_label)
            label_change1h.place(
                x=215, y=55+i*spacing, width=55, height=spacing)
            self.labels_change1h.append(label_change1h)

            label_change5m = tk.Label(
                root, text="-300.76%", justify="center", font=font_label)
            label_change5m.place(
                x=275, y=55+i*spacing, width=55, height=spacing)
            self.labels_change5m.append(label_change5m)

            label_rsi6 = tk.Label(root, text="16.72",
                                  justify="center", font=font_label)
            label_rsi6.place(
                x=335, y=55+i*spacing, width=55, height=spacing)
            self.labels_rsi6.append(label_rsi6)

            label_rsi14 = tk.Label(
                root, text="26.72", justify="center", font=font_label)
            label_rsi14.place(
                x=395, y=55+i*spacing, width=55, height=spacing)
            self.labels_rsi14.append(label_rsi14)

            label_high = tk.Label(root, text="2.3456789",
                                  justify="center", font=font_label)
            label_high.place(
                x=455, y=55+i*spacing, width=55, height=spacing)
            self.labels_high.append(label_high)

            label_low = tk.Label(root, text="0.1234567",
                                 justify="center", font=font_label)
            label_low.place(
                x=515, y=55+i*spacing, width=55, height=spacing)
            self.labels_low.append(label_low)

            btn_chart = tk.Button(root, text="Chart",
                                  justify="center", font=font_label)
            btn_chart.place(x=575, y=55+i*spacing, width=40, height=spacing-2)
            btn_chart["command"] = lambda: self.btn_chart_command(currency)
            self.btns_chart.append(btn_chart)

    def btn_chart_command(self, currency):
        # Open chart window for the given currency
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    sw = MarketWindow(None, root, currencies=[
                      "BTC", "ETH", "BNB", "IOTA", "LTC", "DOT", "ADA", "BCH", "DOGE", "XRP", "BSC", "BNT", "PNY"])
    root.mainloop()
