import pygame


class Button:
    def __init__(self, screen, text, x, y, width, height, color=(20, 33, 61)) -> None:
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.draw()

    def draw(self):
        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=10,
        )
        pygame.font.init()
        font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.x + self.width / 2, self.y + self.height / 2)
        )
        self.screen.blit(text, text_rect)
