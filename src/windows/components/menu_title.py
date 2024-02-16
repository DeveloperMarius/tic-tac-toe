import pygame


class MenuTitle:
    def __init__(
        self,
        title: str,
        x: int,
        y: int,
        font: str = "Lucida Sans",
        color: tuple[int, int, int] = (255, 0, 0),
    ):
        self.title = title
        self.x = x
        self.y = y
        self.font = font
        self.color = color

    def draw(self, screen: pygame.Surface):
        pygame.font.init()
        font = pygame.font.SysFont(self.font, 54, False)
        text = font.render(self.title, True, self.color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
