import pygame

from .components.menu_title import MenuTitle
from .window_manager import Window, WindowManager
from .components.button import Button
from ..game.config import Clients


class MainMenuWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.4 * self.width
        self.menu_height = 0.75 * self.height

        self.menu_title = MenuTitle(
            title="Tic Tac Toe",
            x=self.mid_x,
            y=self.mid_y - self.menu_height / 2 + self.mid_y / 6,
        )

        button_width = 0.8 * self.menu_width
        button_height = 0.1 * self.menu_height
        button_margin = 0.025 * self.menu_height

        self.menu_button_texts = ["Play Online", "Play Offline", "Options", "Exit"]

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
            if button.text == "Play Online":
                if Clients.first().get_username() is None:
                    from random_username.generate import generate_username
                    from .options_window import OptionsWindow

                    Clients.first().set_username(generate_username(1)[0])

                    WindowManager.get_instance().activeWindow = OptionsWindow()
                    return
                from .play_online_window import PlayOnlineWindow

                WindowManager.get_instance().activeWindow = PlayOnlineWindow()

            elif button.text == "Play Offline":
                from .game_difficulty_window import GameDifficultyWindow

                WindowManager.get_instance().activeWindow = GameDifficultyWindow()

            elif button.text == "Options":
                from .options_window import OptionsWindow

                WindowManager.get_instance().activeWindow = OptionsWindow()
            elif button.text == "Exit":
                pygame.quit()
                exit()

    def draw(self, screen):
        for button in self.menu_buttons:
            button.draw()

        self.menu_title.draw(screen)
