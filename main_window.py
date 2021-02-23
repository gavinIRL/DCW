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
        self.newWindowAnalysis = None
        self.newWindowWallet = None
        self.newWindowSettings = None
        self.newWindowAlerts = None
        # set fonts
        ftButton = tkFont.Font(family='Times', size=12)
        ft = tkFont.Font(family='Times', size=12)
        ftStatus = tkFont.Font(family='Times', size=12, weight="bold")
        # setting title
        self.root.title("DCW Main Menu")
        # setting window size
        width = 300
        height = 321
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.btnAnalysis = tk.Button(self.root)
        self.btnAnalysis["font"] = ftButton
        self.btnAnalysis["justify"] = "center"
        self.btnAnalysis["text"] = "Open Analysis Window"
        self.btnAnalysis.place(x=0, y=230, width=width, height=30)
        self.btnAnalysis["command"] = self.btnAnalysis_command

        self.btnSettings = tk.Button(self.root)
        self.btnSettings["font"] = ftButton
        self.btnSettings["justify"] = "center"
        self.btnSettings["text"] = "Open Settings"
        self.btnSettings.place(x=0, y=160, width=width, height=30)
        self.btnSettings["command"] = self.btnSettings_command

        lblBitcoinPrice = tk.Label(self.root)
        lblBitcoinPrice["font"] = ft
        lblBitcoinPrice["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        lblBitcoinPrice["text"] = "Bitcoin price at login: $190"
        lblBitcoinPrice.place(x=0, y=125, width=width, height=30)

        lblStart = tk.Label(self.root)
        lblStart["font"] = ft
        lblStart["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        lblStart["text"] = "Bitcoin: 24hr high $200 | low $180"
        lblStart.place(x=0, y=95, width=width, height=30)

        self.btnWallet = tk.Button(self.root)
        self.btnWallet["font"] = ftButton
        self.btnWallet["justify"] = "center"
        self.btnWallet["text"] = "Open Wallet"
        self.btnWallet.place(x=0, y=195, width=width, height=30)
        self.btnWallet["command"] = self.btnWallet_command

        self.btnAlerts = tk.Button(self.root)
        self.btnAlerts["font"] = ftButton
        self.btnAlerts["justify"] = "center"
        self.btnAlerts["text"] = "Alerts"
        self.btnAlerts.place(x=0, y=290, width=width, height=30)
        self.btnAlerts["command"] = self.btnAlerts_command

        self.lblVPNStatus = tk.Label(self.root)
        self.lblVPNStatus["font"] = ftStatus
        self.lblVPNStatus["justify"] = "center"
        self.lblVPNStatus["text"] = "User Status: " + \
            str(G_Utils.checkSettingsFileExists())
        self.lblVPNStatus.place(x=0, y=5, width=width, height=30)

        self.lblBlockStatus = tk.Label(self.root)
        self.lblBlockStatus["font"] = ftStatus
        self.lblBlockStatus["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        self.lblBlockStatus["text"] = "User Net Worth: $1000"
        self.lblBlockStatus.place(x=0, y=35, width=width, height=30)

        lblBirthday = tk.Label(self.root)
        lblBirthday["font"] = ft
        lblBirthday["justify"] = "center"
        # This gets updated later, but a placeholder for startup
        lblBirthday["text"] = "User 24hr Net Worth Increase: 11%"
        lblBirthday.place(x=0, y=65, width=width, height=30)

    def destroyAnalysis(self):
        self.newWindowAnalysis.destroy()
        self.btnAnalysis["state"] = "normal"

    def destroyWallet(self):
        self.newWindowWallet.destroy()
        self.btnWallet["state"] = "normal"

    def destroySettings(self):
        self.newWindowSettings.destroy()
        self.btnSettings["state"] = "normal"

    def destroyAlerts(self):
        self.newWindowAlerts.destroy()
        self.btnAlerts["state"] = "normal"

    def new_window(self, _class):
        if _class is WalletWindow:
            self.btnWallet["state"] = "disabled"
            self.newWindowWallet = tk.Toplevel(self.root)
            self.newWindowWallet.protocol(
                "WM_DELETE_WINDOW", self.destroyWallet)
            _class(self, self.newWindowWallet)
        if _class is AnalysisWindow:
            self.btnAnalysis["state"] = "disabled"
            self.newWindowAnalysis = tk.Toplevel(self.root)
            self.newWindowAnalysis.protocol(
                "WM_DELETE_WINDOW", self.destroyAnalysis)
            _class(self, self.newWindowAnalysis)
        if _class is SettingsWindow:
            self.btnSettings["state"] = "disabled"
            self.newWindowSettings = tk.Toplevel(self.root)
            self.newWindowSettings.protocol(
                "WM_DELETE_WINDOW", self.destroySettings)
            _class(self, self.newWindowSettings)
        if _class is AlertsWindow:
            self.btnAlerts["state"] = "disabled"
            self.newWindowAlerts = tk.Toplevel(self.root)
            self.newWindowAlerts.protocol(
                "WM_DELETE_WINDOW", self.destroyAlerts)
            _class(self, self.newWindowAlerts)

    def btnSettings_command(self):
        self.new_window(SettingsWindow)

    def btnAlerts_command(self):
        self.new_window(AlertsWindow)

    def btnAnalysis_command(self):
        self.new_window(AnalysisWindow)

    def btnWallet_command(self):
        self.new_window(WalletWindow)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    MainWindow = MainWindow(root)

    def checkPrices():
        # Perform an update of the information
        pass
        root.after(30000, checkPrices)
    root.after(30, checkPrices)
    root.wm_attributes('-topmost', True)
    root.mainloop()
