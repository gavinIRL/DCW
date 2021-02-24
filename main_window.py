import tkinter as tk
import tkinter.font as tkFont
from g_utils import G_Utils
from analysis_window import AnalysisWindow
from wallet_window import WalletWindow
from settings_window import SettingsWindow
from alerts_window import AlertsWindow


class MainWindow():

    def __init__(self, root):
        self.root = root
        # set variables
        self.new_window_analysis = None
        self.new_window_wallet = None
        self.new_window_settings = None
        self.new_window_alerts = None
        # set fonts
        font_button = tkFont.Font(family='Times', size=12)
        ft = tkFont.Font(family='Times', size=12)
        font_status = tkFont.Font(family='Times', size=12, weight="bold")
        # setting title
        self.root.title("DCW Main Menu")
        # setting window size
        width = 300
        height = 321
        width_screen = self.root.winfo_width_screen()
        height_screen = self.root.winfo_height_screen()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (width_screen - width) / 2, (height_screen - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.btn_analysis = tk.Button(self.root)
        self.btn_analysis["font"] = font_button
        self.btn_analysis["justify"] = "center"
        self.btn_analysis["text"] = "Open Analysis Window"
        self.btn_analysis.place(x=0, y=230, width=width, height=30)
        self.btn_analysis["command"] = self.btn_analysis_command

        self.btn_settings = tk.Button(self.root)
        self.btn_settings["font"] = font_button
        self.btn_settings["justify"] = "center"
        self.btn_settings["text"] = "Open Settings"
        self.btn_settings.place(x=0, y=160, width=width, height=30)
        self.btn_settings["command"] = self.btn_settings_command

        self.lbl_bitcoin_price = tk.Label(self.root)
        self.lbl_bitcoin_price["font"] = ft
        self.lbl_bitcoin_price["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_bitcoin_price["text"] = "Bitcoin price at login: $190"
        self.lbl_bitcoin_price.place(x=0, y=125, width=width, height=30)

        self.lbl_bitcoin_hilo = tk.Label(self.root)
        self.lbl_bitcoin_hilo["font"] = ft
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
        self.btn_alerts["text"] = "Alerts"
        self.btn_alerts.place(x=0, y=290, width=width, height=30)
        self.btn_alerts["command"] = self.btn_alerts_command

        self.lbl_user_status = tk.Label(self.root)
        self.lbl_user_status["font"] = font_status
        self.lbl_user_status["justify"] = "center"
        self.lbl_user_status["text"] = "User Status: " + \
            str(G_Utils.checkSettingsFileExists())
        self.lbl_user_status.place(x=0, y=5, width=width, height=30)

        self.lbl_net_worth = tk.Label(self.root)
        self.lbl_net_worth["font"] = font_status
        self.lbl_net_worth["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_net_worth["text"] = "User Net Worth: $1000"
        self.lbl_net_worth.place(x=0, y=35, width=width, height=30)

        self.lbl_net_worth_incr = tk.Label(self.root)
        self.lbl_net_worth_incr["font"] = ft
        self.lbl_net_worth_incr["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lbl_net_worth_incr["text"] = "User 24hr Net Worth Increase: 11%"
        self.lbl_net_worth_incr.place(x=0, y=65, width=width, height=30)

    def destroy_analysis(self):
        self.new_window_analysis.destroy()
        self.btn_analysis["state"] = "normal"

    def destroy_wallet(self):
        self.new_window_wallet.destroy()
        self.btn_wallet["state"] = "normal"

    def destroy_settings(self):
        self.new_window_settings.destroy()
        self.btn_settings["state"] = "normal"

    def destroy_alerts(self):
        self.new_window_alerts.destroy()
        self.btn_alerts["state"] = "normal"

    def new_window(self, _class):
        if _class is WalletWindow:
            self.btn_wallet["state"] = "disabled"
            self.new_window_wallet = tk.Toplevel(self.root)
            self.new_window_wallet.protocol(
                "WM_DELETE_WINDOW", self.destroy_wallet)
            _class(self, self.new_window_wallet)
        if _class is AnalysisWindow:
            self.btn_analysis["state"] = "disabled"
            self.new_window_analysis = tk.Toplevel(self.root)
            self.new_window_analysis.protocol(
                "WM_DELETE_WINDOW", self.destroy_analysis)
            _class(self, self.new_window_analysis)
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

    def btn_settings_command(self):
        self.new_window(SettingsWindow)

    def btn_alerts_command(self):
        self.new_window(AlertsWindow)

    def btn_analysis_command(self):
        self.new_window(AnalysisWindow)

    def btn_wallet_command(self):
        self.new_window(WalletWindow)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    MainWindow = MainWindow(root)

    def update_prices():
        # Perform an update of the information
        # These are all either placeholder or call placeholder functions
        bitcoin_price = G_Utils.get_coin_price(
            G_Utils.get_API_key(), "BTC", "1h")
        bitcoin_price_yesterday = 12
        net_worth_increase = (
            (float(G_Utils.get_net_worth("now", "BTC"))/float(G_Utils.get_net_worth("yesterday", "BTC")))*100)-1

        root.after(30000, update_prices)
    root.after(30, update_prices)
    root.wm_attributes('-topmost', True)
    root.mainloop()
