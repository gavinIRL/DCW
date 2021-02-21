import tkinter as tk
import tkinter.font as tkFont


class WalletWindow:
    def __init__(self, mainwindow, root):
        self.mainwindow = mainwindow
        self.root = root
        self.root.geometry("400x400+400+400")
        self.frame = tk.Frame(self.root)
        self.quitButton = tk.Button(
            self.frame, text='Quit', width=25, command=self.close_windows)
        self.label = tk.Label(root, text=f"this is the wallet window")
        self.label.pack()
        self.label2 = tk.Label(
            root, text="THIS IS HERE TO DIFFERENTIATE THIS WINDOW")
        self.label2.pack()
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.mainwindow.btnAnalysis["state"] = "normal"
        self.root.destroy()
