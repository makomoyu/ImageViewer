from dataclasses import dataclass
from PIL import ImageTk

@dataclass
class CanvasDataClass:
    photo_image:ImageTk.PhotoImage|None = None
    scale:float = 1.0
