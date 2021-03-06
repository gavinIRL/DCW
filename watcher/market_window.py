import tkinter as tk
import tkinter.font as tkFont
from dcw_utils import DCWUtils
from chart_window import ChartWindow
import time
import threading


class MarketWindow:
    def __init__(self, mainwindow, root, currencies):
        self.mainwindow = mainwindow
        self.root = root
        self.currencies = currencies
        # These are for holding the RSI recent values
        self.last_15_opens_5min = []
        self.last_15_opens_1hr = []
        # These variables are for storing the latest data
        # Used for opening chart window from scratch and also pushing updates
        # self.candles = []
        self.prices = []
        self.base_5min = []
        self.base_1hr = []
        self.base_24hr = []
        self.base_1wk = []
        for entry in self.currencies:
            self.prices.append(100)
            self.base_5min.append(100)
            self.base_1hr.append(100)
            self.base_24hr.append(100)
            self.base_1wk.append(100)
            self.last_15_opens_5min.append([100, 200])
            self.last_15_opens_1hr.append([100, 200])
            # might do something with entry after
        # This is used to reduce amount of updates of longer timeframes
        self.colour_update_counter = -3
        self.ticker_update_counter = 1

        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=20, weight="bold")

        width = 796
        height = 476
        alignstr = '%dx%d+%d+%d' % (width, height, 10, 10)
        self.root.geometry(alignstr)

        self.root.resizable(width=False, height=False)
        self.root.title("Market")

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = "Market (Base = USD)"
        self.lbl_title.place(x=0, y=5, width=width, height=25)

        # Then the labels to denote RSI timeframes
        vert_distance = 35
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "5min"
        self.lbl_heading.place(
            x=425, y=vert_distance, width=55, height=20)

        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "1hr"
        self.lbl_heading.place(
            x=545, y=vert_distance, width=55, height=20)

        # Then the labels of the columns of data
        horz_distance = 95
        vert_distance += 20
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "Current"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "5min"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "1hr"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "24hr"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "1wk"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(6)"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(14)"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(6)"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "RSI(14)"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "24High"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        horz_distance += 60
        self.lbl_heading = tk.Label(self.root)
        self.lbl_heading["font"] = font_heading
        self.lbl_heading["justify"] = "center"
        self.lbl_heading["text"] = "24Low"
        self.lbl_heading.place(
            x=horz_distance, y=vert_distance, width=55, height=20)

        self.labels_symbols = []
        self.labels_current = []
        self.labels_change24h = []
        self.labels_change1w = []
        self.labels_change1h = []
        self.labels_change5m = []
        self.labels_rsi6 = []
        self.labels_rsi14 = []
        self.labels_rsi6_1h = []
        self.labels_rsi14_1h = []
        self.labels_high = []
        self.labels_low = []
        self.btns_chart = []
        vert_distance += 20

        for i, currency in enumerate(self.currencies):
            vert_spacing = 40
            horz_distance = 2
            if len(self.currencies) > 10:
                vert_spacing = int(400/len(self.currencies))
            label_symbol = tk.Label(
                root, text=currency, justify="left", font=font_label)
            label_symbol.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=92, height=vert_spacing)
            self.labels_symbols.append(label_symbol)

            horz_distance += 93
            label_current = tk.Label(
                root, text="1.2345678", justify="center", font=font_label)
            label_current.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_current.append(label_current)

            horz_distance += 60
            label_change5m = tk.Label(
                root, text="-300.76%", justify="center", font=font_label)
            label_change5m.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change5m.append(label_change5m)

            horz_distance += 60
            label_change1h = tk.Label(
                root, text="+600.76%", justify="center", font=font_label)
            label_change1h.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change1h.append(label_change1h)

            horz_distance += 60
            label_change24h = tk.Label(
                root, text="+100.76%", justify="center", font=font_label)
            label_change24h.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change24h.append(label_change24h)

            horz_distance += 60
            label_change1w = tk.Label(
                root, text="+500.76%", justify="center", font=font_label)
            label_change1w.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_change1w.append(label_change1w)

            horz_distance += 60
            label_rsi6 = tk.Label(root, text="16.72",
                                  justify="center", font=font_label)
            label_rsi6.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_rsi6.append(label_rsi6)

            horz_distance += 60
            label_rsi14 = tk.Label(
                root, text="26.72", justify="center", font=font_label)
            label_rsi14.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_rsi14.append(label_rsi14)

            horz_distance += 60
            label_rsi6_1h = tk.Label(root, text="46.72",
                                     justify="center", font=font_label)
            label_rsi6_1h.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_rsi6_1h.append(label_rsi6_1h)

            horz_distance += 60
            label_rsi14_1h = tk.Label(
                root, text="56.72", justify="center", font=font_label)
            label_rsi14_1h.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_rsi14_1h.append(label_rsi14_1h)

            horz_distance += 60
            label_high = tk.Label(root, text="2.3456789",
                                  justify="center", font=font_label)
            label_high.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_high.append(label_high)

            horz_distance += 60
            label_low = tk.Label(root, text="0.1234567",
                                 justify="center", font=font_label)
            label_low.place(
                x=horz_distance, y=vert_distance+i*vert_spacing, width=55, height=vert_spacing)
            self.labels_low.append(label_low)

            horz_distance += 60
            btn_chart = tk.Button(root, text="Chart",
                                  justify="center", font=font_label)
            btn_chart["command"] = lambda i=i: self.btn_chart_command(i)
            btn_chart.place(x=horz_distance, y=vert_distance+i*vert_spacing,
                            width=40, height=vert_spacing-2)
            self.btns_chart.append(btn_chart)
        # Then fill out the initial data
        self.startup()
        # And then start updating candles every 2 mins while the window is open
        root.after(1000, self.update_candles(self.mainwindow, self.root))
        # if self.mainwindow:

    def btn_chart_command(self, index):
        # print(index)
        self.mainwindow.new_window(
            _class=ChartWindow, mainwindow=self.mainwindow, currency=self.currencies[index], prices=self.last_15_opens_5min[index])
        # Open chart window for the given currency
        pass

    def startup(self):
        dcw = DCWUtils(exchange="Binance")
        fresh_data = dcw.get_tick(self.mainwindow.market_currency_list)
        self.update_all_prices(fresh_data)

    def rsi_thread_handler(self, pairindex, n_value):
        # EAFP in case window is closed after thread added to queue
        try:
            if len(self.last_15_opens_5min[pairindex]) > 3:
                # First do the 5min RSI values
                data = self.last_15_opens_5min[pairindex]
                # there are 15 or 16 values sent, the correct one is the last one
                value = DCWUtils.get_rsi(data, n=n_value)[-1]
                # if pairindex == 3:
                # print(data)
                colour = "black"
                if value < 30:
                    colour = "green"
                elif value > 70:
                    colour = "red"
                if n_value == 6:
                    self.labels_rsi6[pairindex].configure(text=str(
                        format(value, ".2f")), fg=colour)
                elif n_value == 14:
                    self.labels_rsi14[pairindex].configure(text=str(
                        format(value, ".2f")), fg=colour)

            if len(self.last_15_opens_1hr[pairindex]) > 3:
                # Then do the 1hr RSI values
                # Decided to do it this way as it was clearer that there are 2 updates
                # Rather than playing coding golf
                data = self.last_15_opens_1hr[pairindex]
                # print(data)
                # there are 15 or 16 values sent, the correct one is the last one
                # value = DCWUtils.get_rsi(data, n=n_value)[-1]
                return_value = DCWUtils.get_rsi(data, n=n_value)
                if len(return_value):
                    value = return_value[-1]
                    colour = "black"
                    if value < 30:
                        colour = "green"
                    elif value > 70:
                        colour = "red"
                    if n_value == 6:
                        self.labels_rsi6_1h[pairindex].configure(text=str(
                            format(value, ".2f")), fg=colour)
                    elif n_value == 14:
                        self.labels_rsi14_1h[pairindex].configure(text=str(
                            format(value, ".2f")), fg=colour)
        except:
            print("Window closed before thread could complete")

    def update_rsi(self):
        # Update the RSI values every second ticker update
        if self.ticker_update_counter % 2 == 0:
            for i, pair in enumerate(self.mainwindow.market_currency_list):
                t = threading.Thread(target=self.rsi_thread_handler,
                                     args=(i, 6))
                self.mainwindow.threads.append(t)
                t.start()
                t2 = threading.Thread(target=self.rsi_thread_handler,
                                      args=(i, 14))
                self.mainwindow.threads.append(t2)
                t2.start()

    def update_colours(self):
        labels = [self.labels_change5m, self.labels_change1h,
                  self.labels_change24h, self.labels_change1w]
        threshold = [0.25, 0.5, 1, 2.5]  # These are for 5m, 1h, 1d, 1w
        # Iterate through the labels and update based on positive/negative
        # But only after the first two rounds of updates
        if self.colour_update_counter == 0:
            # Update all
            for index, currency in enumerate(self.currencies):
                for i, label in enumerate(labels):
                    if float(label[index]["text"].replace("%", "")) > threshold[i]:
                        label[index].configure(fg="green")
                    elif float(label[index]["text"].replace("%", "")) < -1 * threshold[i]:
                        label[index].configure(fg="red")
                    else:
                        label[index].configure(fg="black")
        if self.colour_update_counter % 2 == 0:
            # Update 5min
            for index, currency in enumerate(self.currencies):
                if float(self.labels_change5m[index]["text"].replace("%", "")) > threshold[0]:
                    self.labels_change5m[index].configure(fg="green")
                elif float(self.labels_change5m[index]["text"].replace("%", "")) < -1*threshold[0]:
                    self.labels_change5m[index].configure(fg="red")
                else:
                    self.labels_change5m[index].configure(fg="black")
        if self.colour_update_counter % 2 == 0:
            for index, currency in enumerate(self.currencies):
                if float(self.labels_change1h[index]["text"].replace("%", "")) > threshold[1]:
                    self.labels_change1h[index].configure(fg="green")
                elif float(self.labels_change1h[index]["text"].replace("%", "")) < -1*threshold[1]:
                    self.labels_change1h[index].configure(fg="red")
                else:
                    self.labels_change1h[index].configure(fg="black")
            # Update 1hr
        if self.colour_update_counter % 4 == 0:
            for index, currency in enumerate(self.currencies):
                if float(self.labels_change24h[index]["text"].replace("%", "")) > threshold[2]:
                    self.labels_change24h[index].configure(fg="green")
                elif float(self.labels_change24h[index]["text"].replace("%", "")) < -1*threshold[2]:
                    self.labels_change24h[index].configure(fg="red")
                else:
                    self.labels_change24h[index].configure(fg="black")
            # Update 24hr
        if self.colour_update_counter % 4 == 0:
            self.colour_update_counter = 1
            for index, currency in enumerate(self.currencies):
                if float(self.labels_change1w[index]["text"].replace("%", "")) > threshold[3]:
                    self.labels_change1w[index].configure(fg="green")
                elif float(self.labels_change1w[index]["text"].replace("%", "")) < -1*threshold[3]:
                    self.labels_change1w[index].configure(fg="red")
                else:
                    self.labels_change1w[index].configure(fg="black")
            # Update 1w
        self.colour_update_counter += 1

    def update_all_prices(self, data):
        for pair, price in data.items():
            # print("Pair = "+pair+" , Price= "+price)
            index = self.currencies.index(pair)
            self.labels_current[index]["text"] = str(price)
            self.prices[index] = float(price)
            # Now update the percentages also depending on the ticker counter
            if self.ticker_update_counter % 2 == 0:
                base_5m = self.base_5min[index]
                change_percent_5m = 100*(1-(base_5m/float(price)))
                self.labels_change5m[index].configure(text=str(
                    format(change_percent_5m, ".2f"))+"%")
            if self.ticker_update_counter % 2 == 0:
                base_1h = self.base_1hr[index]
                change_percent_1h = 100*(1-(base_1h/float(price)))
                self.labels_change1h[index].configure(text=str(
                    format(change_percent_1h, ".2f"))+"%")
            if self.ticker_update_counter % 4 == 0:
                base_1d = self.base_24hr[index]
                change_percent_1d = 100*(1-(base_1d/float(price)))
                self.labels_change24h[index].configure(text=str(
                    format(change_percent_1d, ".2f"))+"%")
            if self.ticker_update_counter % 4 == 0:
                self.ticker_update_counter = 0
                base_1w = self.base_1wk[index]
                change_percent_1w = 100*(1-(base_1w/float(price)))
                self.labels_change1w[index].configure(text=str(
                    format(change_percent_1w, ".2f"))+"%")
            # And then update the recent RSI value
            # It will comprise of the previous 15 opens and current price
            # Check if there is a 16th value first
            if len(self.last_15_opens_5min[index]) < 3:
                pass
            elif len(self.last_15_opens_5min[index]) < 16:
                self.last_15_opens_5min[index].append(float(price))
            # Otherwise update the 16th value
            else:
                self.last_15_opens_5min[index][-1] = float(price)
            if len(self.last_15_opens_1hr[index]) < 3:
                pass
            elif len(self.last_15_opens_1hr[index]) < 16:
                self.last_15_opens_1hr[index].append(float(price))
            # Otherwise update the 16th value
            else:
                self.last_15_opens_1hr[index][-1] = float(price)
        # And finally do a colour check
        self.update_colours()
        # And a RSI update also
        self.update_rsi()
        self.ticker_update_counter += 1

    def update_percentages_new(self, pair, data_5m, data_1h, data_1d, data_1w, data_hilo):
        index = self.currencies.index(pair)
        current = float(self.prices[index])

        change_percent_5m = 100*(1-(float(data_5m["Open"])/current))
        change_percent_1h = 100*(1-(float(data_1h["Open"])/current))
        change_percent_1d = 100*(1-(float(data_1d["Open"])/current))
        change_percent_1w = 100*(1-(float(data_1w["Open"])/current))
        self.labels_change5m[index].configure(text=str(
            format(change_percent_5m, ".2f"))+"%")
        self.labels_change1h[index].configure(text=str(
            format(change_percent_1h, ".2f"))+"%")
        self.labels_change1w[index].configure(text=str(
            format(change_percent_1w, ".2f"))+"%")
        self.labels_change24h[index].configure(text=str(
            format(change_percent_1d, ".2f"))+"%")
        # Then update the base values to tick against
        self.base_5min[index] = float(data_5m["Open"])
        self.base_1hr[index] = float(data_1h["Open"])
        self.base_24hr[index] = float(data_1d["Open"])
        self.base_1wk[index] = float(data_1w["Open"])
        # Then update the high and low values
        day_high = float(data_hilo["High"])
        day_low = float(data_hilo["Low"])
        self.labels_high[index].configure(text=day_high)
        self.labels_low[index].configure(text=day_low)
        # And also update the mainwindow hilo if pair is bitcoin
        if pair == "BTCUSDT":
            hilo_text = "Bitcoin: 24hr high $" + \
                str(day_high)+" | low $"+str(day_low)
            self.mainwindow.lbl_bitcoin_hilo.configure(text=hilo_text)

    def candle_thread_handler(self, mw, dcw, pair, sleep_timer):
        time.sleep(sleep_timer)
        # EAFP in case window is closed after thread added to queue
        try:
            # Getting smaller chunks
            # Most recent values are always last
            data_5m_1h = dcw.get_candle(pair, "1m", 80)
            data_1d_1w = dcw.get_candle(pair, "1h", 168)
            data_hilo = dcw.get_candle(pair, "1d", 1)
            mw.mw.update_percentages_new(
                pair, data_5m_1h[-5], data_5m_1h[20], data_1d_1w[-24], data_1d_1w[0], data_hilo[0])
            # then update the rsi 5min list
            list_recent_5min = data_5m_1h[::5]
            open_list = []
            for line in list_recent_5min:
                open_list.append(float(line["Open"]))
            self.last_15_opens_5min[self.currencies.index(pair)] = open_list
            # and then update the rsi 1hr list
            list_recent_1hr = data_1d_1w[-15:]
            open_list = []
            for line in list_recent_1hr:
                open_list.append(float(line["Open"]))
            # print(open_list)
            self.last_15_opens_1hr[self.currencies.index(pair)] = open_list
        except:
            print("Window closed before thread could complete")

    def update_candles(self, mw, root):
        # This is last thing called after opening market window
        if self.mainwindow.mw != None:
            # Grab the information
            dcw = DCWUtils("Binance")
            for i, pair in enumerate(self.mainwindow.market_currency_list):
                t = threading.Thread(target=self.candle_thread_handler,
                                     args=(mw, dcw, pair, i*0.25))
                self.mainwindow.threads.append(t)
                t.start()
            # Then make sure to update it every 2.5mins
            root.after(150000, lambda: self.update_candles(mw, root))
        else:
            root.after(500, lambda: self.update_candles(mw, root))


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    sw = MarketWindow(None, root, currencies=[
        "BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "XLMUSDT",
        "BCHUSDT", "DOGEUSDT", "XEMUSDT", "ATOMUSDT", "XMRUSDT", "BSVUSDT", "EOSUSDT"])
    root.mainloop()
