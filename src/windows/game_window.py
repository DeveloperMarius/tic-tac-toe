from time import sleep
from pygame import Surface
import pygame

from ..game.game import Game

from .components.button import Button
from .components.tictactoe_field import TicTacToeField
from .window_manager import Window, WindowManager


class GameWindow(Window):

    def __init__(self, difficulty=0) -> None:
        super().__init__()
        width, height = self.screen.get_size()

        # Aspect ratio 1:1 minus padding
        self.size = min(width, height) - min(width, height) * 0.2

        # Center the field
        self.x = (width - self.size) / 2
        self.y = (height - self.size) / 2

        self.difficulty = difficulty
        self.game = Game(difficulty)

        self.tictactoe_field = TicTacToeField(
            self.screen,
            self.x,
            self.y,
            self.size,
            self.size,
            self.game.handle_turn,
        )

        self.tictactoe_field.field_rects = self.game.handle_ai_first(
            self.tictactoe_field.field_rects
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

        self.winner = None
        self.font = pygame.font.SysFont("Comic Sans MS", 36)
        self.title_font = pygame.font.SysFont("Comic Sans MS", 54)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.winner is not None:
                for button in self.menu_buttons:
                    if not button.rect.collidepoint(event.pos):
                        continue

                    elif button.text == "Restart":
                        print("Restart")
                        WindowManager.get_instance().activeWindow = GameWindow(
                            self.difficulty
                        )
                        return

                    elif button.text == "Main Menu":
                        print("Main Menu")
                        from .main_menu_window import MainMenuWindow

                        WindowManager.get_instance().activeWindow = MainMenuWindow()

            elif winner := self.tictactoe_field.handle_events(event):
                self.winner = winner

    def draw(self, _: Surface):

        # If there is no winner
        if self.winner is None:
            if self.game.current_player.symbol == self.game.player_1.symbol:
                text = self.font.render(
                    f"Your turn ({'O' if self.game.current_player.symbol == 2 else 'X'})",
                    True,
                    (255, 255, 255),
                )
            else:
                text = self.font.render(
                    f"AI turn ({'O' if self.game.current_player.symbol == 2 else 'X'})",
                    True,
                    (255, 255, 255),
                )

            self.tictactoe_field.draw()
            text_rect = text.get_rect()
            text_rect.center = (self.x + self.size / 2, self.y - text_rect.height)
            self.screen.blit(text, text_rect)

        # If there is a winner
        else:
            self.tictactoe_field.draw()
            s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            s.fill((0, 0, 0, 230))
            self.screen.blit(s, (0, 0))

            if self.winner == self.game.player_1.symbol:
                text = self.title_font.render(
                    f"You won! ({'O' if self.winner == 2 else 'X'})",
                    True,
                    (255, 255, 255),
                )
            elif self.winner == self.game.player_2.symbol:
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
