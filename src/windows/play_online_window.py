import pygame
from .window_manager import Window, WindowManager
from .components.menu_button import MenuButton


class PlayOnlineWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.4 * self.width
        self.menu_height = 0.75 * self.height

        button_width = 0.8 * self.menu_width
        button_height = 0.1 * self.menu_height
        button_margin = 0.025 * self.menu_height

        self.menu_button_texts = ["Join", "Host", "Back"]

        self.menu_buttons = [
            MenuButton(
                screen=self.screen,
                text=text,
                x=self.mid_x - button_width / 2,
                y=self.mid_y * 1.25
                - self.menu_height / 2
                + i * button_height
                + button_margin * (i + 1),
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
            if button.text == "Join":
                print("Join")
            elif button.text == "Host":
                print("Host")
            elif button.text == "Back":
                from .main_menu_window import MainMenuWindow

                WindowManager().activeWindow = MainMenuWindow()

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
        font = pygame.font.SysFont("Arial", 48, True)
        text = font.render(b"Play Online", True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(self.mid_x, self.mid_y - self.menu_height / 2 + self.mid_y / 6)
        )
        self.screen.blit(text, text_rect)
