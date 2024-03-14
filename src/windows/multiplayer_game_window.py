import pygame


from .window_manager import Window
from .components.chat_pane import ChatPane
from .components.tictactoe_field import TicTacToeField


class MultiplayerGameWindow(Window):
    def __init__(self):
        super().__init__()

        # self.player_ids = [user._id for user in ClientConfig.get_sessionmanager().users]

        # TODO:
        # - Create ClientGame
        # - Add clientGameTurnHandle() to send network requests to ServerGame on Host
        # self.server_game = ServerGame(self.player_ids)

        # TODO: Delete this and replace with clientGameTurnHandle
        def handle_tictactoefield():
            print("Click")
            return self.tictactoe_field.field_rects

        self.tictactoe_field = TicTacToeField(
            self.screen,
            (0.675 * self.width - (self.height * 0.8)) / 2,
            0 + self.height * 0.1,
            self.height * 0.8,
            self.height * 0.8,
            handle_tictactoefield,  # TODO: CHANGEME
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
