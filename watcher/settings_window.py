import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk


class SettingsWindow:
    def __init__(self, mainwindow, root):
        self.mainwindow = mainwindow
        self.root = root
        self.status_pref_pairs = tk.IntVar()
        self.status_pref_view = tk.IntVar()
        self.status_data_save = tk.IntVar()

        font_button = tkFont.Font(family='Times', size=12)
        font_label = tkFont.Font(family='Times', size=12)
        font_heading = tkFont.Font(family='Times', size=20, weight="bold")

        width = 200
        height = 281
        width_screen = self.root.winfo_screenwidth()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (width_screen - (width*2)), 50)
        self.root.geometry(alignstr)

        self.root.resizable(width=False, height=False)
        self.root.title("Settings")

        self.lbl_title = tk.Label(self.root)
        self.lbl_title["font"] = font_heading
        self.lbl_title["justify"] = "center"
        self.lbl_title["text"] = "Settings"
        self.lbl_title.place(x=0, y=5, width=width, height=50)

        self.btn_pref_pairs = tk.Button(self.root)
        self.btn_pref_pairs["font"] = font_button
        self.btn_pref_pairs["justify"] = "center"
        self.btn_pref_pairs["text"] = "Edit Preferred Pairs"
        self.btn_pref_pairs.place(x=0, y=55, width=width, height=30)
        self.btn_pref_pairs["command"] = self.btn_pref_pairs_command

        self.lbl_exchange = tk.Label(self.root)
        self.lbl_exchange["font"] = font_label
        self.lbl_exchange["justify"] = "left"
        self.lbl_exchange["text"] = "Default Exchange:"
        self.lbl_exchange.place(x=2, y=90, width=120, height=30)

        self.combo_exchange = ttk.Combobox(self.root)
        self.combo_exchange["font"] = font_button
        self.combo_exchange["state"] = "readonly"
        self.combo_exchange["justify"] = "right"
        self.combo_exchange["values"] = ["Binance", "Bitfinex"]
        self.combo_exchange.place(x=125, y=90, width=75, height=30)
        # This will need to be updated based on the settings file later
        self.combo_exchange.current(0)

        self.lbl_base = tk.Label(self.root)
        self.lbl_base["font"] = font_label
        self.lbl_base["justify"] = "left"
        self.lbl_base["text"] = "Base Currency:"
        self.lbl_base.place(x=5, y=120, width=120, height=30)

        self.combo_base = ttk.Combobox(self.root)
        self.combo_base["font"] = font_button
        self.combo_base["state"] = "readonly"
        self.combo_base["justify"] = "center"
        self.combo_base["values"] = ["USD", "BTC", "ETH"]
        self.combo_base.place(x=125, y=120, width=75, height=30)
        # This will need to be updated based on the settings file later
        self.combo_base.current(0)

        self.lbl_refresh = tk.Label(self.root)
        self.lbl_refresh["font"] = font_label
        self.lbl_refresh["justify"] = "left"
        self.lbl_refresh["text"] = "Refresh Rate:"
        self.lbl_refresh.place(x=5, y=150, width=95, height=30)

        self.spin_refresh = ttk.Spinbox(self.root)
        self.spin_refresh["font"] = font_label
        self.spin_refresh["state"] = "readonly"
        self.spin_refresh["justify"] = "center"
        self.spin_refresh["wrap"] = True
        self.spin_refresh["values"] = ["1", "1.5", "2", "2.5",
                                       "3", "4", "5", "10", "15", "20", "30", "45", "60", "120"]
        self.spin_refresh.place(x=95, y=150, width=45, height=30)
        # This will need to be updated based on the settings file later
        self.spin_refresh.set("1")

        self.lbl_refresh_sec = tk.Label(self.root)
        self.lbl_refresh_sec["font"] = font_label
        self.lbl_refresh_sec["justify"] = "left"
        self.lbl_refresh_sec["text"] = "seconds"
        self.lbl_refresh_sec.place(x=140, y=150, width=60, height=30)

        chk_pref_pairs = tk.Checkbutton(root)
        chk_pref_pairs["font"] = font_button
        chk_pref_pairs["justify"] = "center"
        chk_pref_pairs["text"] = "Save Pairs Preferences"
        chk_pref_pairs.place(x=0, y=185, width=width, height=30)
        chk_pref_pairs["offvalue"] = "0"
        chk_pref_pairs["onvalue"] = "1"
        chk_pref_pairs["command"] = self.chk_pref_pairs_command
        chk_pref_pairs["variable"] = self.status_pref_pairs

        chk_pref_view = tk.Checkbutton(root)
        chk_pref_view["font"] = font_button
        chk_pref_view["justify"] = "center"
        chk_pref_view["text"] = "Save View Preferences"
        chk_pref_view.place(x=0, y=215, width=width, height=30)
        chk_pref_view["offvalue"] = "0"
        chk_pref_view["onvalue"] = "1"
        chk_pref_view["command"] = self.chk_pref_view_command
        chk_pref_view["variable"] = self.status_pref_view

        chk_data_save = tk.Checkbutton(root)
        chk_data_save["font"] = font_button
        chk_data_save["justify"] = "center"
        chk_data_save["text"] = "Save Ticker Log to CSV"
        chk_data_save.place(x=0, y=245, width=width, height=30)
        chk_data_save["offvalue"] = "0"
        chk_data_save["onvalue"] = "1"
        chk_data_save["command"] = self.chk_data_save_command
        chk_data_save["variable"] = self.status_data_save

    def btn_pref_pairs_command(self):
        pass

    def chk_pref_pairs_command(self):
        pass

    def chk_pref_view_command(self):
        pass

    def chk_data_save_command(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-toolwindow', True)
    sw = SettingsWindow(None, root)
    root.mainloop()
