import pygame


class WindowManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WindowManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._activeWindow: Window = None

    @property
    def activeWindow(self):
        return self._activeWindow

    @activeWindow.setter
    def activeWindow(self, window):
        del self._activeWindow
        self._activeWindow = window


class Window:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.width, self.height = pygame.display.get_surface().get_size()
        self.mid_x = self.width / 2
        self.mid_y = self.height / 2

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def mid_x(self):
        return self._mid_x

    @mid_x.setter
    def mid_x(self, value):
        self._mid_x = value

    @property
    def mid_y(self):
        return self._mid_y

    @mid_y.setter
    def mid_y(self, value):
        self._mid_y = value

    def handleEvent(self, event):
        pass

    def draw(self, screen: pygame.Surface):
        pass
