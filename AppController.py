from AppModel import AppModel
import cv2
from ImageProcessor import ImageProcessor
import tkinter as tk
from tkinter import filedialog
from CanvasDrawHelper import CanvasDrawHelper


class AppController:
    def __init__(self, model:AppModel):
        
        self.model = model
        self.original_image = None
        self.cut_image = None
        self.binary_image = None
        self.current_image = None
        

    def select_image_file(self, canvas, canvas_data):
        try:
            print("ファイル選択")
            selected_image_path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp")])
            if not selected_image_path:
                return
            self.set_image(selected_image_path)
            CanvasDrawHelper.draw_image(self.original_image, canvas, canvas_data)
        except Exception as ex:
            print(f"エラー：{ex}")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bmp",
            filetypes=[("BMP", "*.bmp"), ("PNG", "*.png"), ("JPG", "*.jpg")]
        )

        if file_path:
            cv2.imwrite(file_path, self.current_image)
            print("保存完了:", file_path)


    def event_mouse_motion(self, event, canvas_data, position_entry, rgb_entry):
        if canvas_data.photo_image is None:
            return
        image_position = CanvasDrawHelper.canvas_to_image_position(event, self.current_image, canvas_data)
        position_entry.delete(0, tk.END)
        position_entry.insert(0, f"{image_position}")

        image_position_color = CanvasDrawHelper.canvas_to_image_color(image_position, self.current_image)
        rgb_entry.delete(0, tk.END)
        rgb_entry.insert(0, f"{image_position_color}")


    def event_mouse_down(self, event, canvas_data):
        if canvas_data.photo_image is None:
            print("画像未選択")
            return
        canvas_data.rectangle = (event.x,event.y,event.x,event.y)

    def event_mouse_dragging(self, event, canvas_data, canvas):
        if canvas_data.photo_image is None:
            print("画像未選択ドラッグ")
            return
        x1, y1, _, _ = canvas_data.rectangle
        canvas_data.rectangle = (x1,y1,event.x,event.y)
        canvas.delete("selection")
        canvas.create_rectangle(canvas_data.rectangle,outline="red",width=2,tags="selection")

    def event_mouse_release(self, canvas_data, ):
        if canvas_data.photo_image is None:
            print("画像未選択リリース")
            return
        image_area = (CanvasDrawHelper.rectangle_to_image_area(canvas_data, self.current_image))
        print(image_area)
        self.set_cut_area(image_area)

    def event_cut_image_button_click(self, canvas_data, canvas):
        if canvas_data.photo_image is None:
            print("画像未選択切り取り")
            return
        self.get_cut_image()
        CanvasDrawHelper.draw_image(self.current_image, canvas, canvas_data)

    def event_change_binary_button_click(self, canvas_data, canvas):
        if canvas_data.photo_image is None:
            print("画像未選択2値化")
            return
        self.change_binary()
        CanvasDrawHelper.draw_image(self.current_image, canvas, canvas_data)

    def event_reset_button_click(self, canvas_data, canvas):
        if canvas_data.photo_image is None:
            print("画像未選択リセット")
            return
        self.current_image = self.original_image.copy()
        CanvasDrawHelper.draw_image(self.current_image, canvas, canvas_data)

    def event_detect_area_button_click(self, canvas_data, canvas):
        if canvas_data.photo_image is None:
            print("画像未選択領域検出")
            return
        self.detect_area()
        CanvasDrawHelper.draw_image(self.current_image, canvas, canvas_data)

    def event_calucate_mean_button_click(self, canvas_data, mean_entry):
        if canvas_data.photo_image is None:
            print("画像未選択平均値計算")
            return
        mean_value = self.calculate_mean_value()
        print(f"平均値: {mean_value}")
        mean_entry.delete(0, tk.END)
        mean_entry.insert(0, f"{mean_value}")
 
 




    def set_image(self, image_path):
        self.original_image = cv2.imread(image_path)
        self.current_image = cv2.imread(image_path)


    def set_cut_area(self, image_cut_area):
        self.cut_image_area = image_cut_area
        
    def get_cut_image(self):
        if self.current_image is None:
            print("画像未選択切り取り")
            return
        x1, y1, x2, y2 = self.cut_image_area
        self.current_image = self.current_image[y1:y2, x1:x2]
        self.cut_image = self.current_image.copy()
        
    def change_binary(self):
        if self.current_image is None:
            print("画像未選択2値化")
            return
        print(self.current_image.shape)
        self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        _, self.current_image = cv2.threshold(self.current_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.binary_image = self.current_image.copy()
    
    def detect_area(self):
        if self.current_image is None:
            print("画像未選択領域検出")
            return
        self.current_image = ImageProcessor.extract_largest_region(self.cut_image, self.binary_image)
        
    def calculate_mean_value(self):
        """
        画像の平均値を計算する
        """
        if self.current_image is None:
            print("画像未選択平均値計算")
            return None
        mean_value = ImageProcessor.calculate_mean_value(self.current_image)
        return mean_value
        