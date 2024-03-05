class BaseComponent:

    def __init__(self) -> None:
        pass

    def draw(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handleEvent(self, event):
        raise NotImplementedError
