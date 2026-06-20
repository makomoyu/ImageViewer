import tkinter as tk
from tkinter import ttk, filedialog
from AppController import AppController
from CreateGridWidgetHelper import CreateGridWidgetHelper

class AppView(tk.Tk):
    def __init__(self, controller:AppController):
        super().__init__()
        self.title("ImageViewer")
        self.state("zoomed")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([0,1], weight=1) 
        self._create_widget()

    
    def _create_widget(self):
        self.canvas_frame = CreateGridWidgetHelper.tk_frame(self, rowconfigure=[0], columnconfigure=[0])
        self.image_view_canvas = CreateGridWidgetHelper.canvas(self.canvas_frame)
        self.button_frame = CreateGridWidgetHelper.tk_frame(self, position=(1,0), rowconfigure=[0], columnconfigure=[0], relief=tk.SUNKEN)

