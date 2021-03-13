import threading
import tkinter as tk
import tkinter.font as tkFont
from dcw_utils import DCWUtils
from chart_window import ChartWindow
from wallet_window import WalletWindow
from settings_window import SettingsWindow
from alerts_window import AlertsWindow
from market_window import MarketWindow
import queue
import time
import threading


class MainWindow():

    def __init__(self, root):
        self.root = root

        # Testing variables
        # self.test_button = tk.Button(
        #    self.root, command=self.tb_click, text="Test")
        #self.test_button.place(x=0, y=230, width=300, height=30)
        self.threads = []

        # set variables for handling windows
        self.new_window_chart = None
        self.new_window_wallet = None
        self.new_window_settings = None
        self.new_window_alerts = None
        self.new_window_market = None
        # this will hold the marketwindow itself
        self.mw = None
        # set variables that hold the settings
        self.update_time = 1000
        self.market_currency_list = [
            "BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "XLMUSDT",
            "BCHUSDT", "DOGEUSDT", "XEMUSDT", "ATOMUSDT", "XMRUSDT", "EOSUSDT", "TRXUSDT"]
        # This is for csv logging
        self.enable_logging = False
        self.log_loop_tracker = -5
        self.fresh_prices = []
        for curr in self.market_currency_list:
            self.fresh_prices.append(1.2)
        # This is for holding the wallet details
        self.current_wallet = []
        # set fonts
        font_button = tkFont.Font(family='Times', size=12)
        font_label = tkFont.Font(family='Times', size=12)
        font_status = tkFont.Font(family='Times', size=12, weight="bold")
        # setting title
        self.root.title("DCW Main Menu")
        # setting window size
        width = 300
        height = 331
        width_screen = self.root.winfo_screenwidth()
        height_screen = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (width_screen - width) / 2, (height_screen - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # self.btn_chart = tk.Button(self.root)
        # self.btn_chart["font"] = font_button
        # self.btn_chart["justify"] = "center"
        # self.btn_chart["text"] = "Open Chart Window"
        # self.btn_chart.place(x=0, y=230, width=width, height=30)
        # self.btn_chart["command"] = self.btn_chart_command

        self.btn_settings = tk.Button(self.root)
        self.btn_settings["font"] = font_button
        self.btn_settings["justify"] = "center"
        self.btn_settings["text"] = "Open Settings"
        self.btn_settings.place(x=0, y=160, width=width, height=30)
        self.btn_settings["command"] = self.btn_settings_command

        self.lbl_bitcoin_price = tk.Label(self.root)
        self.lbl_bitcoin_price["font"] = font_label
        self.lbl_bitcoin_price["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_bitcoin_price["text"] = "Bitcoin price: $190"
        self.lbl_bitcoin_price.place(x=0, y=125, width=width, height=30)

        self.lbl_bitcoin_hilo = tk.Label(self.root)
        self.lbl_bitcoin_hilo["font"] = font_label
        self.lbl_bitcoin_hilo["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_bitcoin_hilo["text"] = "Bitcoin: 24hr high $200 | low $180"
        self.lbl_bitcoin_hilo.place(x=0, y=95, width=width, height=30)

        self.btn_wallet = tk.Button(self.root)
        self.btn_wallet["font"] = font_button
        self.btn_wallet["justify"] = "center"
        self.btn_wallet["text"] = "Open Wallet"
        self.btn_wallet.place(x=0, y=195, width=width, height=30)
        self.btn_wallet["command"] = self.btn_wallet_command

        self.btn_alerts = tk.Button(self.root)
        self.btn_alerts["font"] = font_button
        self.btn_alerts["justify"] = "center"
        self.btn_alerts["text"] = "Open Alerts"
        self.btn_alerts.place(x=0, y=300, width=width, height=30)
        self.btn_alerts["command"] = self.btn_alerts_command

        self.lbl_user_status = tk.Label(self.root)
        self.lbl_user_status["font"] = font_status
        self.lbl_user_status["justify"] = "center"
        self.lbl_user_status["text"] = "User Setup Complete: " + \
            str(DCWUtils.checkSettingsFileExists())
        self.lbl_user_status.place(x=0, y=5, width=width, height=30)

        self.lbl_net_worth = tk.Label(self.root)
        self.lbl_net_worth["font"] = font_status
        self.lbl_net_worth["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_net_worth["text"] = "User Net Worth: $1000"
        self.lbl_net_worth.place(x=0, y=35, width=width, height=30)

        self.btn_market = tk.Button(self.root)
        self.btn_market["font"] = font_button
        self.btn_market["justify"] = "center"
        self.btn_market["text"] = "Open Market Overview"
        self.btn_market.place(x=0, y=265, width=width, height=30)
        self.btn_market["command"] = self.btn_market_command

        self.lbl_net_worth_incr = tk.Label(self.root)
        self.lbl_net_worth_incr["font"] = font_label
        self.lbl_net_worth_incr["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_net_worth_incr["text"] = "User 24hr Net Worth Increase: 11%"
        self.lbl_net_worth_incr.place(x=0, y=65, width=width, height=30)

    def destroy_wallet(self):
        self.new_window_wallet.destroy()
        self.btn_wallet["state"] = "normal"

    def destroy_settings(self):
        self.new_window_settings.destroy()
        self.btn_settings["state"] = "normal"

    def destroy_alerts(self):
        self.new_window_alerts.destroy()
        self.btn_alerts["state"] = "normal"

    def destroy_market(self):
        self.new_window_market.destroy()
        self.btn_market["state"] = "normal"
        self.new_window_market = None
        self.mw = None

    def new_window(self, _class, **kwargs):
        if _class is WalletWindow:
            self.btn_wallet["state"] = "disabled"
            self.new_window_wallet = tk.Toplevel(self.root)
            self.new_window_wallet.protocol(
                "WM_DELETE_WINDOW", self.destroy_wallet)
            _class(self, self.new_window_wallet)
        if _class is ChartWindow:
            # self.btn_chart["state"] = "disabled"
            self.new_window_chart = tk.Toplevel(self.root)
            # self.new_window_chart.protocol(
            #     "WM_DELETE_WINDOW", self.destroy_analysis)
            _class(master=self.new_window_chart, **kwargs)
        if _class is SettingsWindow:
            self.btn_settings["state"] = "disabled"
            self.new_window_settings = tk.Toplevel(self.root)
            self.new_window_settings.protocol(
                "WM_DELETE_WINDOW", self.destroy_settings)
            _class(self, self.new_window_settings)
        if _class is AlertsWindow:
            self.btn_alerts["state"] = "disabled"
            self.new_window_alerts = tk.Toplevel(self.root)
            self.new_window_alerts.protocol(
                "WM_DELETE_WINDOW", self.destroy_alerts)
            _class(self, self.new_window_alerts)
        if _class is MarketWindow:
            self.btn_market["state"] = "disabled"
            self.new_window_market = tk.Toplevel(self.root)
            self.new_window_market.protocol(
                "WM_DELETE_WINDOW", self.destroy_market)
            self.mw = _class(self, self.new_window_market,
                             currencies=self.market_currency_list)

    def btn_settings_command(self):
        self.new_window(SettingsWindow)

    def btn_alerts_command(self):
        self.new_window(AlertsWindow)

    # def btn_chart_command(self):
    #     self.new_window(ChartWindow)

    def btn_wallet_command(self):
        self.new_window(WalletWindow)

    def btn_market_command(self):
        self.new_window(MarketWindow)

    def update_bitcoin_price(self, price=1337):
        self.lbl_bitcoin_price["text"] = "Bitcoin price: $"+str(price)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    MainWindow = MainWindow(root)
    dcw = DCWUtils(exchange="Binance")
    # Having this as a function for readability only

    def startup():
        # Perform the startup functions such as grabbing settings
        # The prices will be grabbed in update prices so no need to do anything here
        # Only going to update the bitcoin hilo once
        dcw = DCWUtils("Binance")
        data_hilo = dcw.get_candle("BTCUSDT", "1d", 1)[0]
        day_high = float(data_hilo["High"])
        day_low = float(data_hilo["Low"])
        hilo_text = "Bitcoin: 24hr high $" + \
            str(day_high)+" | low $"+str(day_low)
        MainWindow.lbl_bitcoin_hilo["text"] = hilo_text

    def update_prices():
        # Perform an update of the information
        # These are all either placeholder or call placeholder functions
        # If the market window isn't open then update at a slower rate of once per 15 seconds
        ticker_time = 5000
        if MainWindow.new_window_market != None:
            ticker_time = MainWindow.update_time
            # Then update the prices in the market window
            current_time = time.time()
            fresh_data = dcw.get_tick(MainWindow.market_currency_list)

            # Update the relevant windows
            MainWindow.mw.update_all_prices(fresh_data)
            MainWindow.update_bitcoin_price(fresh_data["BTCUSDT"])

            if MainWindow.enable_logging:
                # Prepare data for logging in csv
                for pair, price in fresh_data.items():
                    index = MainWindow.market_currency_list.index(pair)
                    MainWindow.fresh_prices[index] = price
                # And then send the data for logging after the first few loops
                # Will eventually make it so that it starts appending to a new file every hour
                if MainWindow.log_loop_tracker > 0:
                    dcw.csv_logger(pairs=MainWindow.market_currency_list, time_list=[
                        current_time], existing_data=[MainWindow.fresh_prices])
                # Will do something like grab a create a new file every day later
                MainWindow.log_loop_tracker += 1

        # Otherwise grab the data and update mainwindow only
        else:
            MainWindow.update_bitcoin_price(dcw.get_tick("BTCUSDT"))
            # And clear any leftover buffer data from previous windows
            MainWindow.log_loop_tracker = -5
            dcw.buffer_counter = 0
            dcw.buffer_data = []
            dcw.buffer_times = []
            dcw.log_start_time = 0

        root.after(ticker_time, update_prices)

    # Now perform the startup process and update as required
    root.after(500, startup)
    root.after(1000, update_prices)
    root.wm_attributes('-topmost', True)
    root.mainloop()
