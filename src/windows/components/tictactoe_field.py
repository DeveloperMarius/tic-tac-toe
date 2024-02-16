import pygame
from .base_component import BaseComponent


class TicTacToeField(BaseComponent):
    def __init__(
        self,
        screen,
        x: int,
        y: int,
        width: int,
        height: int,
        handle_turn: callable,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.handle_turn = handle_turn

        # Lines
        self.lines = [
            (
                (self.x + self.width * 1 / 3, self.y),
                (self.x + self.width * 1 / 3, self.y + self.height),
            ),
            (
                (self.x + self.width * 2 / 3, self.y),
                (self.x + self.width * 2 / 3, self.y + self.height),
            ),
            (
                (self.x, self.y + self.height * 1 / 3),
                (self.x + self.width, self.y + self.height * 1 / 3),
            ),
            (
                (self.x, self.y + self.height * 2 / 3),
                (self.x + self.width, self.y + self.height * 2 / 3),
            ),
        ]

        # Collide Rects
        self.field_rects = [
            FieldRect(
                self.x,
                self.y,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x + self.width * 1 / 3,
                self.y,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x + self.width * 2 / 3,
                self.y,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x,
                self.y + self.height * 1 / 3,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x + self.width * 1 / 3,
                self.y + self.height * 1 / 3,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x + self.width * 2 / 3,
                self.y + self.height * 1 / 3,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x,
                self.y + self.height * 2 / 3,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x + self.width * 1 / 3,
                self.y + self.height * 2 / 3,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
            FieldRect(
                self.x + self.width * 2 / 3,
                self.y + self.height * 2 / 3,
                self.width * 1 / 3,
                self.height * 1 / 3,
            ),
        ]

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        self._field = value

    def handle_events(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        for i, field_rect in enumerate(self.field_rects):
            if not field_rect.rect.collidepoint(event.pos):
                continue

            if field_rect.checked != 0:
                # TODO: Add a message that the field is already checked
                print("Field already checked")
                break

            # Return the index of the field and the rects to let the game handle the turn
            self.field_rects = self.handle_turn(i, self.field_rects)
            break

    def draw(self):

        # Collide Rects
        for rect in self.field_rects:
            rect.draw(self.screen)

        # Lines
        for line in self.lines:
            pygame.draw.line(self.screen, self.color, line[0], line[1], 2)


class FieldRect:
    def __init__(self, x, y, width, height, checked: int = 0, padding: int = 10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.checked = checked
        self.rect = None
        self.padding = padding

    def draw(self, screen):
        self.rect = pygame.draw.rect(
            screen, (255, 255, 255), (self.x, self.y, self.width, self.height)
        )

        match self.checked:

            case 1:
                # Draw X
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (self.x + self.padding, self.y + self.padding),
                    (
                        self.x + self.width - self.padding,
                        self.y + self.height - self.padding,
                    ),
                    2,
                )
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (self.x + self.width - self.padding, self.y + self.padding),
                    (self.x + self.padding, self.y + self.height - self.padding),
                    2,
                )

            case 2:
                # Draw O
                pygame.draw.ellipse(
                    screen,
                    (0, 0, 0),
                    (
                        self.x + self.padding,
                        self.y + self.padding,
                        self.width - self.padding,
                        self.height - self.padding,
                    ),
                    2,
                )
