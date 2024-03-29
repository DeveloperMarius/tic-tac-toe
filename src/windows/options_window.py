import pygame


from .window_manager import Window, WindowManager
from .components.button import Button
from .components.menu_title import MenuTitle
from .components.input import Input
from ..game.config import Clients
from ..game.events import Event, EventType
from ..game.network import NetworkClient


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

        self.username_input = Input(
            screen=self.screen,
            x=self.mid_x - button_width / 2,
            y=self.mid_y * 1.25
            - self.menu_height / 2
            + button_margin
            + button_height
            + 10,
            width=button_width,
            height=button_height,
            padding=(button_height - 38),
            text=Clients.first().get_username(),
        )

        self.menu_buttons = [
            Button(
                self.screen,
                "Save",
                self.mid_x - button_width / 2,
                self.mid_y * 1.25
                - self.menu_height / 2
                + 2 * button_height
                + button_margin * 2
                + 10,
                button_width,
                button_height,
                color=(129, 215, 126),
            ),
            Button(
                self.screen,
                "Back",
                self.mid_x - button_width / 2,
                self.mid_y * 1.25
                - self.menu_height / 2
                + 3 * button_height
                + button_margin * 3
                + 10,
                button_width,
                button_height,
            ),
        ]

    def handleEvent(self, event):
        self.username_input.handle_events(event)

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        for button in self.menu_buttons:
            if not button.rect.collidepoint(event.pos):
                continue
            elif button.text == "Save":
                if Clients.first().get_username() == self.username_input.text:
                    continue

                Clients.first().set_username(self.username_input.text)
                # Implement success message
            elif button.text == "Back":
                from .main_menu_window import MainMenuWindow

                WindowManager.get_instance().activeWindow = MainMenuWindow()

    def draw(self, screen):

        self.menu_buttons[0].color = (
            (99, 99, 99)
            if Clients.first().get_username() == self.username_input.text
            else (129, 215, 126)
        )

        username_label = pygame.font.SysFont(pygame.font.get_default_font(), 24).render(
            "Username:", True, (255, 255, 255)
        )
        self.screen.blit(
            username_label,
            (
                self.username_input.rect.x,
                self.username_input.rect.y
                - username_label.get_height()
                - 0.0125 * self.menu_height,
            ),
        )

        self.username_input.draw()

        for button in self.menu_buttons:
            button.draw()

        self.menu_title.draw(screen)
