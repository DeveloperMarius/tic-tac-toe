from pygame import Surface
from .window_manager import Window


class GameWindow(Window):

    def __init__(self) -> None:
        super().__init__()

    def handleEvent(self, event):
        pass

    def draw(self, screen: Surface):
        pass
