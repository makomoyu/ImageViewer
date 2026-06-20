import tkinter as tk
from tkinter import ttk, filedialog
from AppController import AppController
from CreateGridWidgetHelper import CreateGridWidgetHelper
from CanvasDataClass import CanvasDataClass
from CanvasDrawHelper import CanvasDrawHelper

import cv2

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
        self._bind_canvas_event()

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
            if not selected_image_path:
                return
            self.controller.set_image(selected_image_path)
            CanvasDrawHelper.draw_image(self.controller.original_image, self.image_view_canvas, self.image_view_canvas_data)
            
            
            
        except Exception as ex:
            print(f"エラー：{ex}")


    def _bind_canvas_event(self):
        self.image_view_canvas.bind("<Button-1>", self.event_mouse_down)
        self.image_view_canvas.bind("<B1-Motion>", self.event_mouse_move)
        self.image_view_canvas.bind("<ButtonRelease-1>", self.event_mouse_release)



    def event_mouse_down(self, event):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択")
            return
        self.image_view_canvas_data.rectangle = (event.x,event.y,event.x,event.y)

    def event_mouse_move(self, event):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択ドラッグ")
            return
        x1, y1, _, _ = self.image_view_canvas_data.rectangle
        self.image_view_canvas_data.rectangle = (x1,y1,event.x,event.y)
        self.image_view_canvas.delete("selection")
        self.image_view_canvas.create_rectangle(self.image_view_canvas_data.rectangle,outline="red",width=2,tags="selection")

    def event_mouse_release(self, event):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択リリース")
            return
        image_area = (CanvasDrawHelper.rectangle_to_image_area(self.image_view_canvas_data, self.controller.current_image))
        print(image_area)
        x1, y1, x2, y2 = image_area
        self.controller.current_image = self.controller.current_image[y1:y2, x1:x2]
        CanvasDrawHelper.draw_image(self.controller.current_image, self.image_view_canvas, self.image_view_canvas_data)