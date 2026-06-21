import tkinter as tk
from tkinter import ttk

class CreateGridWidgetHelper:
    
    @staticmethod
    def tk_frame(root, position=(0,0), rowspan=1, colunmspan=1, sticky="news", rowconfigure=None, columnconfigure=None, relief=None):
        colunm, row = position
        tk_frame = tk.Frame(root, relief=relief)
        tk_frame.grid(row=row, column=colunm, rowspan=rowspan, columnspan=colunmspan, sticky="news")
        tk_frame.rowconfigure(rowconfigure, weight=1)
        tk_frame.columnconfigure(columnconfigure, weight=1)
        return tk_frame
    
    @staticmethod
    def canvas(root, background="#222222", position=(0,0)):
        colunm, row = position
        canvas = tk.Canvas(root, background=background)
        canvas.grid(row=row, column=colunm, sticky="news")
        return canvas
    
    @staticmethod
    def ttk_button(root, text, command=None, position=(0,0)):
        colunm, row = position
        button = ttk.Button(root, text=text, command=command)
        button.grid(row=row, column=colunm)
        return button