from pygame import Surface
import pygame

from ..game.game import Game

from .components.tictactoe_field import TicTacToeField
from .window_manager import Window


class GameWindow(Window):

    def __init__(self) -> None:
        super().__init__()
        width, height = self.screen.get_size()

        # Aspect ratio 1:1 minus padding
        self.size = min(width, height) - min(width, height) * 0.2

        # Center the field
        self.x = (width - self.size) / 2
        self.y = (height - self.size) / 2

        self.game = Game()

        self.tictactoe_field = TicTacToeField(
            self.screen,
            self.x,
            self.y,
            self.size,
            self.size,
            self.game.handle_turn,
        )

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.tictactoe_field.handle_events(event)

    def draw(self, _: Surface):
        self.tictactoe_field.draw()
