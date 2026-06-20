import tkinter as tk
from AppController import AppController

class AppView(tk.Tk):
    def __init__(self, controller:AppController):
        super().__init__()
        self.title("ImageViewer")
        