import pygame

from .window_manager import Window, WindowManager
from .components.button import Button
from .components.menu_title import MenuTitle
from .components.ip_input import IPInput
from ..game.config import ClientConfig
from ..game.network import NetworkClient, NetworkServer


class PlayOnlineWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.4 * self.width
        self.menu_height = 0.75 * self.height

        self.menu_title = MenuTitle(
            title="Play Online",
            x=self.mid_x,
            y=self.mid_y - self.menu_height / 2 + self.mid_y / 6,
        )

        button_width = 0.8 * self.menu_width
        button_height = 0.1 * self.menu_height
        button_margin = 0.025 * self.menu_height

        self.menu_input = IPInput(
            screen=self.screen,
            x=self.mid_x - button_width / 2,
            y=self.mid_y * 1.25 - self.menu_height / 2 + button_margin + 10,
            width=button_width,
            height=button_height,
            text="Enter IP Address",
        )

        self.menu_button_texts = ["Join", "Host", "Back"]

        self.menu_buttons = [
            Button(
                screen=self.screen,
                text=text,
                x=self.mid_x - button_width / 2,
                y=self.mid_y * 1.25
                - self.menu_height / 2
                + (i + 1) * button_height
                + button_margin * (i + 2)
                + 10,
                width=button_width,
                height=button_height,
            )
            for i, text in enumerate(self.menu_button_texts)
        ]

        self.menu_items = [self.menu_input] + self.menu_buttons

    def handleEvent(self, event):
        self.menu_input.handle_events(event)

        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.menu_buttons:
                if not button.rect.collidepoint(event.pos):
                    continue
                if button.text == "Join":
                    print("Join")
                    print(self.menu_input.text)
                    # todo check if valid ip
                    if self.menu_input.text == "Enter IP Address":
                        return
                    ClientConfig.username = "USERNAME2"
                    NetworkClient.get_instance().connect(ClientConfig.username, self.menu_input.text)
                    # todo start game window
                    from .lobby_window import LobbyWindow
                    WindowManager().activeWindow = LobbyWindow()
                    LobbyWindow().lobby_pane.player_name = ClientConfig.username
                elif button.text == "Host":

                    NetworkServer().start_server()
                    # TODO SET USERNAME
                    ClientConfig.username = "USERNAME"
                    NetworkClient.get_instance().connect(ClientConfig.username, '127.0.0.1')

                    from .lobby_window import LobbyWindow

                    WindowManager().activeWindow = LobbyWindow()
                    LobbyWindow().host_name = ClientConfig.username
                elif button.text == "Back":
                    from .main_menu_window import MainMenuWindow

                    WindowManager().activeWindow = MainMenuWindow()

    def draw(self, screen):
        for item in self.menu_items:
            item.draw()

        self.menu_title.draw(screen)
