import tkinter as tk
from PIL import Image
from PIL import ImageTk
import numpy as np
import cv2

from CanvasDataClass import CanvasDataClass


class CanvasDrawHelper:

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

        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        photo_image = ImageTk.PhotoImage(pil_image)
        # photo_image = ImageTk.PhotoImage(resized_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2,canvas_height // 2,image=photo_image,anchor=tk.CENTER)

        # canvas_data.image = image
        canvas_data.scale = scale
        canvas_data.photo_image = photo_image