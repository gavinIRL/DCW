import tkinter as tk
import tkinter.font as tkFont


class MarketWindow:
    def __init__(self, mainwindow, root):
        self.mainwindow = mainwindow
        self.root = root
        self.root.geometry("400x400+400+400")
        self.frame = tk.Frame(self.root)
        self.label = tk.Label(root, text=f"this is the market window")
        self.label.pack()
        self.label2 = tk.Label(
            root, text="THIS IS HERE TO DIFFERENTIATE THIS WINDOW")
        self.label2.pack()
        self.frame.pack()
