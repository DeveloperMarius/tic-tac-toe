import pygame


from .window_manager import Window
from .components.chat_pane import ChatPane
from .components.tictactoe_field import TicTacToeField, FieldRect
from ..game.events import Event, EventType
from ..game.network import NetworkClient


class MultiplayerGameWindow(Window):
    def __init__(self):
        super().__init__()

        def handle_tictactoefield(index: int, fields: list[FieldRect]):
            NetworkClient.first().send(
                Event(
                    EventType.GAMEPLAY_MOVE_RESPONSE, {"x": index % 3, "y": index // 3}
                )
            )
            return fields

        self.tictactoe_field = TicTacToeField(
            self.screen,
            (0.675 * self.width - (self.height * 0.8)) / 2,
            0 + self.height * 0.1,
            self.height * 0.8,
            self.height * 0.8,
            handle_tictactoefield,
        )
        self.chat_pane = ChatPane(
            self.screen,
            0.675 * self.width,
            0 + self.height * 0.1,
            0.25 * self.width,
            self.height * 0.8,
        )

    def draw(self, _: pygame.Surface):
        self.tictactoe_field.draw()
        self.chat_pane.draw()

    def handleEvent(self, event):
        self.chat_pane.handleEvent(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.tictactoe_field.handle_events(event)
