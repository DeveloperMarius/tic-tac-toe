import pygame


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
