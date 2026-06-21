from AppModel import AppModel
import cv2
from ImageProcessor import ImageProcessor

class AppController:
    def __init__(self, model:AppModel):
        
        self.model = model
        self.original_image = None
        self.cut_image = None
        self.binary_image = None
        self.current_image = None
        

    def set_image(self, image_path):
        self.original_image = cv2.imread(image_path)
        self.current_image = cv2.imread(image_path)


    def set_cut_area(self, image_cut_area):
        self.cut_image_area = image_cut_area
        
    def decide_cut_image(self):
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
        