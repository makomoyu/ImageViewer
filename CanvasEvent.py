import tkinter as tk
from CanvasDrawHelper import CanvasDrawHelper

class CanvasEvent:

    def motion(event, canvas_data, position_entry, rgb_entry, image):
        if canvas_data.photo_image is None:
            return
        image_position = CanvasDrawHelper.canvas_to_image_position(event, image, canvas_data)
        position_entry.delete(0, tk.END)
        position_entry.insert(0, f"{image_position}")

        image_position_color = CanvasDrawHelper.canvas_to_image_color(image_position, image)
        rgb_entry.delete(0, tk.END)
        rgb_entry.insert(0, f"{image_position_color}")


    def down(event, canvas_data):
        if canvas_data.photo_image is None:
            print("画像未選択")
            return
        canvas_data.rectangle = (event.x,event.y,event.x,event.y)

    def dragging(event, canvas_data, canvas):
        if canvas_data.photo_image is None:
            print("画像未選択ドラッグ")
            return
        x1, y1, _, _ = canvas_data.rectangle
        canvas_data.rectangle = (x1,y1,event.x,event.y)
        canvas.delete("selection")
        canvas.create_rectangle(canvas_data.rectangle,outline="red",width=2,tags="selection")

    def release(canvas_data, image, set_handler):
        if canvas_data.photo_image is None:
            print("画像未選択リリース")
            return
        image_area = (CanvasDrawHelper.rectangle_to_image_area(canvas_data, image))
        print(image_area)
        set_handler(image_area)