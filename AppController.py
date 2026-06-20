from AppModel import AppModel
import cv2

class AppController:
    def __init__(self, model:AppModel):
        
        self.original_image = None
        self.current_image = None

    
    def set_image(self, image_path):
        self.original_image = cv2.imread(image_path)
        self.current_image = cv2.imread(image_path)


    def event_cut_image_button_click(self):
        a=0