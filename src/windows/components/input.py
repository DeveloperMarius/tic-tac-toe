import pygame


class Input:

    def __init__(self, screen, text, x, y, width, height, color=(222, 22, 11)) -> None:
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=10,
        )

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self):
        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=10,
        )
        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans MS", 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.x + self.width / 2, self.y + self.height / 2)
        )
        self.screen.blit(text, text_rect)
