import tkinter as tk
import tkinter.font as tkFont


class WalletWindow:
    def __init__(self, mainwindow, root):
        self.mainwindow = mainwindow
        self.root = root
        font_heading = tkFont.Font(family='Times', size=10, weight="bold")
        font_label = tkFont.Font(family='Times', size=10)
        font_title = tkFont.Font(family='Times', size=20, weight="bold")

        width = 300
        height = 331
        alignstr = '%dx%d+%d+%d' % (width, height, 10, 10)
        self.root.geometry(alignstr)

        self.root.resizable(width=False, height=False)
        self.root.title("Wallet")

        vert_position = 5
        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_title
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = "Wallet"
        self.lbl_title.place(x=0, y=vert_position, width=width, height=25)

        vert_position += 30
        self.lbl_net_worth = tk.Label(self.root)
        self.lbl_net_worth["font"] = font_heading
        self.lbl_net_worth["justify"] = "center"
        self.lbl_net_worth["text"] = "Current Net Worth: $0.00"
        self.lbl_net_worth.place(x=0, y=vert_position, width=width, height=20)

        vert_position += 20
        self.lbl_pnl_1d = tk.Label(self.root)
        self.lbl_pnl_1d["font"] = font_heading
        self.lbl_pnl_1d["justify"] = "center"
        self.lbl_pnl_1d["text"] = "Profit/Loss Past 24hrs: $0.00 | 0.00%"
        self.lbl_pnl_1d.place(x=0, y=vert_position, width=width, height=20)

        vert_position += 20
        self.lbl_pnl_1w = tk.Label(self.root)
        self.lbl_pnl_1w["font"] = font_heading
        self.lbl_pnl_1w["justify"] = "center"
        self.lbl_pnl_1w["text"] = "Profit/Loss Past 7 days: $0.00 | 0.00%"
        self.lbl_pnl_1w.place(x=0, y=vert_position, width=width, height=20)

        vert_position += 20
        self.lbl_pnl_1m = tk.Label(self.root)
        self.lbl_pnl_1m["font"] = font_heading
        self.lbl_pnl_1m["justify"] = "center"
        self.lbl_pnl_1m["text"] = "Profit/Loss Past 30 days: $0.00 | 0.00%"
        self.lbl_pnl_1m.place(x=0, y=vert_position, width=width, height=20)

        vert_position += 20
        self.lbl_pnl_all_time = tk.Label(self.root)
        self.lbl_pnl_all_time["font"] = font_heading
        self.lbl_pnl_all_time["justify"] = "center"
        self.lbl_pnl_all_time["text"] = "Profit/Loss all-time: $0.00 | 0.00%"
        self.lbl_pnl_all_time.place(
            x=0, y=vert_position, width=width, height=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    ww = WalletWindow(None, root)
    root.mainloop()
