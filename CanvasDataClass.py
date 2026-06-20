from dataclasses import dataclass
from PIL import ImageTk

@dataclass
class CanvasDataClass:
    photo_image:ImageTk.PhotoImage|None = None
    scale:float = 1.0
    rectangle: tuple[int, int, int, int] | None = None
    display_x:int = 0
    display_y:int = 0