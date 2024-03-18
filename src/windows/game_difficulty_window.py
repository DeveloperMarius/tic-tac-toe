import pygame


from .window_manager import Window, WindowManager
from .components.button import Button
from .components.menu_title import MenuTitle


class GameDifficultyWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.4 * self.width
        self.menu_height = 0.75 * self.height

        self.menu_title = MenuTitle(
            title="Wähle den Schwierigkeitsgrad",
            x=self.mid_x,
            y=self.mid_y - self.menu_height / 2 + self.mid_y / 6,
        )

        button_width = 0.8 * self.menu_width
        button_height = 0.1 * self.menu_height
        button_margin = 0.025 * self.menu_height

        self.menu_button_texts = ["Einfach", "Schwer"]

        self.menu_buttons = [
            Button(
                screen=self.screen,
                text=text,
                x=self.mid_x - button_width / 2,
                y=self.mid_y * 1.3
                - self.menu_height / 2
                + i * button_height
                + button_margin * (i + 1)
                + 10,
                width=button_width,
                height=button_height,
            )
            for i, text in enumerate(self.menu_button_texts)
        ]

    def handleEvent(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        for button in self.menu_buttons:
            if not button.rect.collidepoint(event.pos):
                continue
            elif button.text == "Einfach":
                from .game_window import GameWindow

                WindowManager.get_instance().activeWindow = GameWindow()
            elif button.text == "Schwer":
                from .game_window import GameWindow

                WindowManager.get_instance().activeWindow = GameWindow(1)

    def draw(self, screen):

        for button in self.menu_buttons:
            button.draw()

        self.menu_title.draw(screen)
