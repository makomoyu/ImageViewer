import tkinter as tk
from tkinter import filedialog
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
        file_menu.add_command(label="保存", command=self.save_image)
        file_menu.add_command(label="終了", command=self.exit_app)

        menu_bar.add_cascade(label="メニュー", menu=file_menu)
        self.config(menu=menu_bar)
        

    def _create_widget(self):

        # キャンバス配置
        self.canvas_frame = CreateGridWidgetHelper.tk_frame(self, rowconfigure=[0], columnconfigure=[0])
        self.image_view_canvas = CreateGridWidgetHelper.canvas(self.canvas_frame)
        
        # ボタン配置
        self.button_frame = CreateGridWidgetHelper.tk_frame(self, position=(1,0), rowconfigure=[0,1,2,3,4], columnconfigure=[0], relief=tk.SUNKEN)
        self.cut_image_button = CreateGridWidgetHelper.ttk_button(self.button_frame, text="切り取り", command=self.event_cut_image_button_click, position=(0,0))
        self.change_binary_button = CreateGridWidgetHelper.ttk_button(self.button_frame, text="2値化", command=self.event_change_binary_button_click, position=(0,1))
        self.detect_area_button = CreateGridWidgetHelper.ttk_button(self.button_frame, text="領域検出", command=self.event_detect_area_button_click, position=(0,2))
        self.calucate_mean_button = CreateGridWidgetHelper.ttk_button(self.button_frame, text="平均値計算", command=self.event_calucate_mean_button_click, position=(0,3))
        self.reset_button = CreateGridWidgetHelper.ttk_button(self.button_frame, text="リセット", command=self.event_reset_button_click, position=(0,4))

        # 情報表示用エントリ配置
        self.image_data_frame = CreateGridWidgetHelper.tk_frame(self, position=(0,1), rowconfigure=0, relief=tk.SUNKEN)
        self.image_data_frame.columnconfigure([1,3,5], weight=1)
        
        self.image_position_entry = CreateGridWidgetHelper.ttk_label_and_entry(self.image_data_frame, label_text="image_xy：", position=(0,0))
        self.image_rgb_entry = CreateGridWidgetHelper.ttk_label_and_entry(self.image_data_frame, label_text="rgb：", position=(2,0) )
        self.image_mean_entry = CreateGridWidgetHelper.ttk_label_and_entry(self.image_data_frame, label_text="image_mean：", position=(4,0))

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

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bmp",
            filetypes=[("BMP files", "*.bmp"), ("PNG files", "*.png"), ("JPG files", "*.jpg")]
        )

        if file_path:
            cv2.imwrite(file_path, self.controller.current_image)
            print("保存完了:", file_path)

    def exit_app(self):
        self.destroy()


    def _bind_canvas_event(self):
        self.image_view_canvas.bind("<Motion>", self.event_mouse_motion)
        self.image_view_canvas.bind("<Button-1>", self.event_mouse_down)
        self.image_view_canvas.bind("<B1-Motion>", self.event_mouse_dragging)
        self.image_view_canvas.bind("<ButtonRelease-1>", self.event_mouse_release)


    def event_mouse_motion(self, event):
        if self.image_view_canvas_data.photo_image is None:
            return
        image_position = CanvasDrawHelper.canvas_to_image_position(event, self.controller.current_image, self.image_view_canvas_data)
        self.image_position_entry.delete(0, tk.END)
        self.image_position_entry.insert(0, f"{image_position}")

        image_position_color = CanvasDrawHelper.canvas_to_image_color(image_position, self.controller.current_image)
        self.image_rgb_entry.delete(0, tk.END)
        self.image_rgb_entry.insert(0, f"{image_position_color}")

    def event_mouse_down(self, event):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択")
            return
        self.image_view_canvas_data.rectangle = (event.x,event.y,event.x,event.y)

    def event_mouse_dragging(self, event):
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
        self.controller.set_cut_area(image_area)
        
    def event_cut_image_button_click(self):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択切り取り")
            return
        self.controller.decide_cut_image()
        CanvasDrawHelper.draw_image(self.controller.current_image, self.image_view_canvas, self.image_view_canvas_data)
        
    def event_change_binary_button_click(self):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択2値化")
            return
        self.controller.change_binary()
        CanvasDrawHelper.draw_image(self.controller.current_image, self.image_view_canvas, self.image_view_canvas_data)
        
    def event_reset_button_click(self):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択リセット")
            return
        self.controller.current_image = self.controller.original_image.copy()
        CanvasDrawHelper.draw_image(self.controller.current_image, self.image_view_canvas, self.image_view_canvas_data)
    
    def event_detect_area_button_click(self):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択領域検出")
            return
        self.controller.detect_area()
        CanvasDrawHelper.draw_image(self.controller.current_image, self.image_view_canvas, self.image_view_canvas_data)
    
    def event_calucate_mean_button_click(self):
        if self.image_view_canvas_data.photo_image is None:
            print("画像未選択平均値計算")
            return
        mean_value = self.controller.calculate_mean_value()
        print(f"平均値: {mean_value}")
        self.image_mean_entry.delete(0, tk.END)
        self.image_mean_entry.insert(0, f"{mean_value}")
    