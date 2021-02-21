import tkinter as tk
import tkinter.font as tkFont
from g_utils import G_Utils
from datetime import datetime
import os


class App:

    def __init__(self, root):
        # set variables
        self.status_block = tk.IntVar()
        self.status_VPN = tk.IntVar()
        # set fonts
        ftButton = tkFont.Font(family='Times', size=16)
        ft = tkFont.Font(family='Times', size=13)
        ftStatus = tkFont.Font(family='Times', size=16, weight="bold")
        # setting title
        root.title("Helper")
        # setting window size
        width = 200
        height = 321
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        btnSites = tk.Button(root)
        btnSites["font"] = ftButton
        btnSites["justify"] = "center"
        btnSites["text"] = "Open X"
        btnSites.place(x=0, y=230, width=200, height=30)
        btnSites["command"] = self.btnSites_command

        chkBlock = tk.Checkbutton(root)
        chkBlock["font"] = ftButton
        chkBlock["justify"] = "center"
        chkBlock["text"] = "Checkbox"
        chkBlock.place(x=0, y=260, width=200, height=31)
        chkBlock["offvalue"] = "0"
        chkBlock["onvalue"] = "1"
        chkBlock["command"] = self.chkBlock_command
        chkBlock["variable"] = self.status_block

        btnLog = tk.Button(root)
        btnLog["font"] = ftButton
        btnLog["justify"] = "center"
        btnLog["text"] = "Open X"
        btnLog.place(x=0, y=160, width=200, height=30)
        btnLog["command"] = self.btnLog_command

        lblChristmas = tk.Label(root)
        lblChristmas["font"] = ft
        lblChristmas["justify"] = "center"
        lblChristmas["text"] = str(
            G_Utils.days_until_christmas()) + " days until Christmas"
        lblChristmas.place(x=0, y=125, width=200, height=30)

        lblStart = tk.Label(root)
        lblStart["font"] = ft
        lblStart["justify"] = "center"
        lblStart["text"] = "Status"
        lblStart.place(x=0, y=95, width=200, height=30)

        btnVPN = tk.Button(root)
        btnVPN["font"] = ftButton
        btnVPN["justify"] = "center"
        btnVPN["text"] = "Start X"
        btnVPN.place(x=0, y=195, width=200, height=30)
        btnVPN["command"] = self.btnVPN_command

        btnClose = tk.Button(root)
        btnClose["font"] = ftButton
        btnClose["justify"] = "center"
        btnClose["text"] = "Close"
        btnClose.place(x=0, y=290, width=200, height=30)
        btnClose["command"] = self.btnClose_command

        self.lblVPNStatus = tk.Label(root)
        self.lblVPNStatus["font"] = ftStatus
        self.lblVPNStatus["justify"] = "center"
        self.lblVPNStatus["text"] = "Status"
        self.lblVPNStatus.place(x=0, y=5, width=200, height=30)

        self.lblBlockStatus = tk.Label(root)
        self.lblBlockStatus["font"] = ftStatus
        self.lblBlockStatus["justify"] = "center"
        self.lblBlockStatus["text"] = "Status"
        self.lblBlockStatus.place(x=0, y=35, width=200, height=30)

        lblBirthday = tk.Label(root)
        lblBirthday["font"] = ft
        lblBirthday["justify"] = "center"
        lblBirthday["text"] = "Status"
        lblBirthday.place(x=0, y=65, width=200, height=30)

    def btnSites_command(self):
        pass

    def chkBlock_command(self):
        if self.status_block.get():
            pass
        else:
            pass

    def btnLog_command(self):
        pass

    def btnClose_command(self):
        # then close
        root.destroy()

    def btnVPN_command(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    app = App(root)

    def checkVPNConnect():
        pass
        root.after(30000, checkVPNConnect)
    root.after(30, checkVPNConnect)
    root.wm_attributes('-topmost', True)
    root.mainloop()
