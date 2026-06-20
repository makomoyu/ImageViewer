import tkinter as tk
from AppModel import AppModel
from AppController import AppController
from AppView import AppView


def start_app():
    app_model = AppModel()
    app_controller = AppController(app_model)
    app_view = AppView(app_controller)
    app_view.mainloop()


if __name__ == "__main__":
    start_app()