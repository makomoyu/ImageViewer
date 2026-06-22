from tkinter import filedialog
from CanvasDrawHelper import CanvasDrawHelper
import cv2

class MenuEvent:

    def select_image_file(canvas, canvas_data, function):
        print("ファイル選択")
        selected_image_path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp")])
        if not selected_image_path:
            return
        image = function(selected_image_path)
        CanvasDrawHelper.draw_image(image, canvas, canvas_data)

    def save_image(image):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bmp",
            filetypes=[("BMP", "*.bmp"), ("PNG", "*.png"), ("JPG", "*.jpg")]
        )

        if file_path:
            cv2.imwrite(file_path, image)
            print("保存完了:", file_path)
        
