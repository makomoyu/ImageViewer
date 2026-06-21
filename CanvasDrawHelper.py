import tkinter as tk
from PIL import Image
from PIL import ImageTk
import numpy as np
import cv2
from CanvasDataClass import CanvasDataClass

def canvas_to_image_coordinate(canvas_x: int,canvas_y: int,canvas_data: CanvasDataClass, image) -> tuple[int, int]:
    image_x = int((canvas_x - canvas_data.display_x)/ canvas_data.scale)
    image_y = int((canvas_y - canvas_data.display_y)/ canvas_data.scale)
    image_height, image_width = (image.shape[:2])
    image_x = max(0,min(image_x, image_width - 1))
    image_y = max(0,min(image_y, image_height - 1))
    return image_x, image_y

class CanvasDrawHelper:

    @staticmethod
    def canvas_to_image_color(image_position, image):
        image_x, image_y = image_position
        b,g,r = image[image_y, image_x]
        return int(r), int(g), int(b)

    @staticmethod
    def canvas_to_image_position(event, image, canvas_data):
        event_x = event.x
        event_y = event.y
        return canvas_to_image_coordinate(event_x, event_y, canvas_data, image)

    @staticmethod
    def rectangle_to_image_area(canvas_data: CanvasDataClass, image) -> tuple[int, int, int, int]:

        if canvas_data.rectangle is None:
            raise ValueError("rectangle が設定されていません")

        x1, y1, x2, y2 = (canvas_data.rectangle)

        image_x1, image_y1 = (canvas_to_image_coordinate(x1,y1,canvas_data, image))
        image_x2, image_y2 = (canvas_to_image_coordinate(x2,y2,canvas_data, image))

        left_top_x = min(image_x1,image_x2)
        left_top_y = min(image_y1,image_y2)
        right_bottom_x = max(image_x1,image_x2)
        right_bottom_y = max(image_y1,image_y2)

        return (left_top_x,left_top_y,right_bottom_x,right_bottom_y)
    


    @staticmethod
    def draw_image(image:np.ndarray,canvas: tk.Canvas,canvas_data: CanvasDataClass) -> None:
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        image_height, image_width = image.shape[:2]
        # image_width = image.width
        # image_height = image.height
        scale_x = canvas_width / image_width
        scale_y = canvas_height / image_height
        scale = min(scale_x, scale_y)
        resize_width = int(image_width * scale)
        resize_height = int(image_height * scale)
        resized_image = cv2.resize(image, (resize_width, resize_height),interpolation=cv2.INTER_NEAREST)
        # resized_image = image.resize((resize_width, resize_height),Image.Resampling.NEAREST)

        display_x = (canvas_width - resize_width) // 2
        display_y = (canvas_height - resize_height) // 2
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        photo_image = ImageTk.PhotoImage(pil_image)
        # photo_image = ImageTk.PhotoImage(resized_image)
        canvas.delete("all")
        canvas.create_image(display_x,display_y,image=photo_image,anchor=tk.NW)
        # canvas.create_image(canvas_width // 2,canvas_height // 2,image=photo_image,anchor=tk.CENTER)

        # canvas_data.image = image

        canvas_data.display_x = display_x
        canvas_data.display_y = display_y
        canvas_data.scale = scale
        canvas_data.photo_image = photo_image