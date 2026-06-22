from AppModel import AppModel
import cv2
from ImageProcessor import ImageProcessor
from CanvasEvent import CanvasEvent
from ButtonEvent import ButtonEvent
from MenuEvent import MenuEvent


class AppController:
    def __init__(self, model:AppModel):
        
        self.model = model
        self.original_image = None
        self.cut_image = None
        self.binary_image = None
        self.current_image = None
        

    def select_image_file(self, canvas, canvas_data):
        MenuEvent.select_image_file(canvas, canvas_data, self.set_image)

    def save_image(self):
        MenuEvent.save_image(self.current_image)

    def event_mouse_motion(self, event, canvas_data, position_entry, rgb_entry):
        CanvasEvent.motion(event, canvas_data, position_entry, rgb_entry, self.current_image)

    def event_mouse_down(self, event, canvas_data):
        CanvasEvent.down(event, canvas_data)

    def event_mouse_dragging(self, event, canvas_data, canvas):
        CanvasEvent.dragging(event, canvas_data, canvas)

    def event_mouse_release(self, canvas_data):
        CanvasEvent.release(canvas_data, self.current_image, self.set_cut_area)

    def event_cut_image_button_click(self, canvas_data, canvas):
        ButtonEvent.cut(canvas_data, canvas, self.get_cut_image)

    def event_change_binary_button_click(self, canvas_data, canvas):
        ButtonEvent.binary(canvas_data, canvas, self.get_binary_image)

    def event_reset_button_click(self, canvas_data, canvas):
        ButtonEvent.reset(canvas_data, canvas, self.refresh_image)

    def event_detect_area_button_click(self, canvas_data, canvas):
        ButtonEvent.area(canvas_data, canvas, self.detect_area)

    def event_calucate_mean_button_click(self, canvas_data, mean_entry):
        ButtonEvent.mean(canvas_data, mean_entry, self.calculate_mean_value)

    def refresh_image(self):
        self.current_image = self.original_image.copy()
        return self.current_image

    def set_image(self, image_path):
        self.original_image = cv2.imread(image_path)
        self.current_image = cv2.imread(image_path)
        return self.original_image


    def set_cut_area(self, image_cut_area):
        self.cut_image_area = image_cut_area
        
    def get_cut_image(self):
        if self.current_image is None:
            print("画像未選択切り取り")
            return
        x1, y1, x2, y2 = self.cut_image_area
        self.current_image = self.current_image[y1:y2, x1:x2]
        self.cut_image = self.current_image.copy()
        return self.cut_image

    def get_binary_image(self):
        if self.current_image is None:
            print("画像未選択2値化")
            return
        print(self.current_image.shape)
        self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        _, self.current_image = cv2.threshold(self.current_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.binary_image = self.current_image.copy()
        return self.binary_image
    
    def detect_area(self):
        if self.current_image is None:
            print("画像未選択領域検出")
            return
        self.current_image = ImageProcessor.extract_largest_region(self.cut_image, self.binary_image)
        return self.current_image
        
    def calculate_mean_value(self):
        """
        画像の平均値を計算する
        """
        if self.current_image is None:
            print("画像未選択平均値計算")
            return None
        mean_value = ImageProcessor.calculate_mean_value(self.current_image)
        return mean_value
        