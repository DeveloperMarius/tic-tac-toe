import pygame

from .window_manager import Window, WindowManager
from .components.button import Button
from .components.menu_title import MenuTitle


class OptionsWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.4 * self.width
        self.menu_height = 0.75 * self.height

        self.menu_title = MenuTitle(
            title="Options",
            x=self.mid_x,
            y=self.mid_y - self.menu_height / 2 + self.mid_y / 6,
        )

        button_width = 0.8 * self.menu_width
        button_height = 0.1 * self.menu_height
        button_margin = 0.025 * self.menu_height

        self.menu_button_texts = ["Back"]

        self.menu_buttons = [
            Button(
                self.screen,
                text,
                self.mid_x - button_width / 2,
                self.mid_y * 1.25
                - self.menu_height / 2
                + i * button_height
                + button_margin * (i + 1)
                + 10,
                button_width,
                button_height,
            )
            for i, text in enumerate(self.menu_button_texts)
        ]

    def handleEvent(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        for button in self.menu_buttons:
            if not button.rect.collidepoint(event.pos):
                continue
            if button.text == "Play":
                print("Play")
            elif button.text == "Options":
                print("Options")
            elif button.text == "Back":
                from .main_menu_window import MainMenuWindow

                WindowManager().activeWindow = MainMenuWindow()

    def draw(self, screen):
        for button in self.menu_buttons:
            button.draw()

        self.menu_title.draw(screen)
