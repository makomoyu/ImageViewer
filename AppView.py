import tkinter as tk
from tkinter import ttk, filedialog
from AppController import AppController
from CreateGridWidgetHelper import CreateGridWidgetHelper
from CanvasDataClass import CanvasDataClass
from CanvasDrawHelper import CanvasDrawHelper

class AppView(tk.Tk):
    def __init__(self, controller:AppController):
        super().__init__()

        self.controller = controller
        self.image_view_canvas_data = CanvasDataClass()
        self.title("ImageViewer")
        self.state("zoomed")
        # self.geometry("1200x800")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([0,1], weight=1) 
        self._create_widget()
        self._create_menu()

    def _create_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="画像選択", command=self.select_image_file)
        file_menu.add_command(label="保存")
        file_menu.add_command(label="終了")

        menu_bar.add_cascade(label="メニュー", menu=file_menu)
        self.config(menu=menu_bar)
        

    def _create_widget(self):

        # キャンバス配置
        self.canvas_frame = CreateGridWidgetHelper.tk_frame(self, rowconfigure=[0], columnconfigure=[0])
        self.image_view_canvas = CreateGridWidgetHelper.canvas(self.canvas_frame)
        
        # ボタン配置
        self.button_frame = CreateGridWidgetHelper.tk_frame(self, position=(1,0), rowconfigure=[0,1,2], columnconfigure=[0], relief=tk.SUNKEN)
        
        self.cut_image_button = ttk.Button(self.button_frame, text="切り取り")
        self.cut_image_button.grid(row=0, column=0)

        self.change_binary_button = ttk.Button(self.button_frame, text="2値化")
        self.change_binary_button.grid(row=1, column=0)

        self.detect_area_button = ttk.Button(self.button_frame, text="領域検出")
        self.detect_area_button.grid(row=2, column=0)


    def select_image_file(self):
        try:
            print("ファイル選択")
            selected_image_path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp")])
            if selected_image_path is None:
                return
            self.controller.set_image(selected_image_path)
            CanvasDrawHelper.draw_image(self.controller.original_image, self.image_view_canvas, self.image_view_canvas_data)
            
            
            
        except Exception as ex:
            print(f"エラー：{ex}")