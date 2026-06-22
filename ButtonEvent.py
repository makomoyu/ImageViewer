import tkinter as tk
from CanvasDrawHelper import CanvasDrawHelper

class ButtonEvent:

    def cut(canvas_data, canvas, function):
        if canvas_data.photo_image is None:
            print("画像未選択切り取り")
            return
        CanvasDrawHelper.draw_image(function(), canvas, canvas_data)

    def binary(canvas_data, canvas, function):
        if canvas_data.photo_image is None:
            print("画像未選択2値化")
            return
        CanvasDrawHelper.draw_image(function(), canvas, canvas_data)

    def reset(canvas_data, canvas, function):
        if canvas_data.photo_image is None:
            print("画像未選択リセット")
            return
        current_image =  function()
        CanvasDrawHelper.draw_image(current_image, canvas, canvas_data)

    def area(canvas_data, canvas, function):
        if canvas_data.photo_image is None:
            print("画像未選択領域検出")
            return
        CanvasDrawHelper.draw_image(function(), canvas, canvas_data)

    def mean(canvas_data, mean_entry, function):
        if canvas_data.photo_image is None:
            print("画像未選択平均値計算")
            return
        mean_value = function()
        print(f"平均値: {mean_value}")
        mean_entry.delete(0, tk.END)
        mean_entry.insert(0, f"{mean_value}")