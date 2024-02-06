import pygame
from window_manager import Window, WindowManager
from windows.options_window import OptionsWindow


class MainMenuWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.4 * self.width
        self.menu_height = 0.75 * self.height

        button_width = 0.8 * self.menu_width
        button_height = 0.15 * self.menu_height
        button_margin = 0.05 * self.menu_height

        self.menu_buttons = [
            MenuButton(
                self.screen,
                "Play",
                self.mid_x - button_width / 2,
                self.mid_y * 1.25 - self.menu_height / 2 + button_margin,
                button_width,
                button_height,
            ),
            MenuButton(
                self.screen,
                "Options",
                self.mid_x - button_width / 2,
                self.mid_y * 1.25
                - self.menu_height / 2
                + button_height
                + button_margin * 2,
                button_width,
                button_height,
            ),
            MenuButton(
                self.screen,
                "Exit",
                self.mid_x - button_width / 2,
                self.mid_y * 1.25
                - self.menu_height / 2
                + 2 * button_height
                + button_margin * 3,
                button_width,
                button_height,
            ),
        ]

    def handleEvent(self, event):
        for button in self.menu_buttons:
            if not button.rect.collidepoint(event.pos):
                continue
            if button.text == "Play":
                print("Play")
            elif button.text == "Options":
                print("Changing Windows")
                WindowManager().activeWindow = OptionsWindow()
            elif button.text == "Exit":
                pygame.quit()

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (222, 223, 232),
            (
                self.mid_x - self.menu_width / 2,
                self.mid_y - self.menu_height / 2,
                self.menu_width,
                self.menu_height,
            ),
            border_radius=10,
        )

        for button in self.menu_buttons:
            button.draw()

        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans MS", 72, True)
        text = font.render(b"Sudoku", False, (255, 0, 0))
        text_rect = text.get_rect(
            center=(self.mid_x, self.mid_y - self.menu_height / 2 + self.mid_y / 6)
        )
        self.screen.blit(text, text_rect)


class MenuButton:
    def __init__(self, screen, text, x, y, width, height) -> None:
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        self.rect = pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (self.x, self.y, self.width, self.height),
            border_radius=10,
        )
        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans MS", 36)
        text = font.render(self.text, True, (0, 122, 122))
        text_rect = text.get_rect(
            center=(self.x + self.width / 2, self.y + self.height / 2)
        )
        self.screen.blit(text, text_rect)
