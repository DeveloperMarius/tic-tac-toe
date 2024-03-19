import pygame


from .window_manager import Window, WindowManager
from .components.button import Button
from .components.chat_pane import ChatPane
from .components.tictactoe_field import TicTacToeField
from ..game.network import NetworkClient, NetworkServer


class MultiplayerGameEndWindow(Window):
    def __init__(self, field_rects, winner, current_player):
        super().__init__()
        self.winner = winner
        self.current_player = current_player

        self.tictactoe_field = TicTacToeField(
            self.screen,
            (0.675 * self.width - (self.height * 0.8)) / 2,
            0 + self.height * 0.1,
            self.height * 0.8,
            self.height * 0.8,
            lambda _: None,
        )
        self.tictactoe_field.field_rects = field_rects

        self.chat_pane = ChatPane(
            self.screen,
            0.675 * self.width,
            0 + self.height * 0.1,
            0.25 * self.width,
            self.height * 0.8,
        )

        button_width = 0.2 * self.width
        button_height = 0.75 * 0.1 * self.height

        self.menu_buttons = [
            Button(
                self.screen,
                "Restart",
                self.mid_x - button_width - 10,
                self.mid_y,
                button_width,
                button_height,
            ),
            Button(
                self.screen,
                "Main Menu",
                self.mid_x + 10,
                self.mid_y,
                button_width,
                button_height,
            ),
        ]

    def draw(self, _: pygame.Surface):
        self.tictactoe_field.draw()
        s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 230))
        self.screen.blit(s, (0, 0))

        if self.winner == self.current_player:
            text = self.title_font.render(
                f"You won! ({'O' if self.winner == 2 else 'X'})",
                True,
                (255, 255, 255),
            )
        elif self.winner == self.current_player:
            text = self.title_font.render(
                f"AI won! ({'O' if self.winner == 2 else 'X'})",
                True,
                (255, 255, 255),
            )
        else:
            text = self.title_font.render("Draw!", True, (255, 255, 255))

        text_rect = text.get_rect()
        text_rect.center = (
            self.x + self.size / 2,
            self.height / 2 - text_rect.height * 1.5,
        )
        self.screen.blit(text, text_rect)
        for button in self.menu_buttons:
            button.draw()
        self.chat_pane.draw()

    def handleEvent(self, event):
        self.chat_pane.handleEvent(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons:
                if not button.rect.collidepoint(event.pos):
                    continue

                elif button.text == "Back to Lobby":
                    from .lobby_window import LobbyWindow

                    WindowManager.get_instance().activeWindow = LobbyWindow()
                    return

                elif button.text == "Main Menu":
                    print("Main Menu")
                    from .main_menu_window import MainMenuWindow

                    NetworkClient.get_instance().disconnect()
                    if NetworkServer.get_instance().running:
                        NetworkServer.get_instance().shutdown()
                    print("Reloading ...")

                    WindowManager.get_instance().activeWindow = MainMenuWindow()
