from threading import Timer
import pygame


class NotificationManager:

    _static_window_manager = None

    @staticmethod
    def get_instance():
        if NotificationManager._static_window_manager is None:
            NotificationManager._static_window_manager = NotificationManager()
        return NotificationManager._static_window_manager

    def __init__(self):
        self._message = None
        self._color = (255, 0, 0)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        timer = Timer(1, self.unset_message)
        timer.start()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def unset_message(self):
        self._message = None
        self._color = (255, 0, 0)

    def long_information(self, message):
        self._message = message
        self._color = (255, 255, 255)

    def reset(self):
        self._message = None
        self._color = (255, 0, 0)

    def draw(self, screen):
        if self._message is not None:
            s = pygame.Surface(
                (screen.get_width(), screen.get_height()), pygame.SRCALPHA
            )
            s.fill((0, 0, 0, 160))
            screen.blit(s, (0, 0))

            font = pygame.font.SysFont("Comic Sans MS", 36)
            text = font.render(self._message, True, self._color)
            text_rect = text.get_rect()
            text_rect.center = (
                screen.get_width() / 2,
                screen.get_height() / 2,
            )
            screen.blit(text, text_rect)
