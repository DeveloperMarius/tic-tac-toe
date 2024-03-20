from threading import Timer
import pygame


class IPInput:

    def __init__(self, screen, text, x, y, width, height, color=(20, 33, 61)) -> None:
        self.screen = screen
        self.text = text
        self.textchanged = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.activeblink = True
        self.cursor_blink()
        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=10,
        )

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if self.active:
                if not self.textchanged:
                    self.text = ""
                    self.textchanged = True

                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def cursor_blink(self):
        self.activeblink = not self.activeblink
        timer = Timer(0.5, self.cursor_blink)
        timer.start()

    def draw(self):

        # Black border
        if self.active:
            self.boder = pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                border_radius=10,
            )

        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=10,
        )

        pygame.font.init()
        font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
        text = font.render(self.text, True, (255, 255, 255))
        ip_text = font.render(":7571", True, (255, 255, 255))

        text_rect = text.get_rect(
            center=(
                self.x + self.width / 2 - ip_text.get_width() / 2,
                self.y + self.height / 2,
            )
        )
        ip_text_rect = text.get_rect(
            topleft=(text_rect.topright[0] + 2, text_rect.topright[1])
        )

        self.screen.blit(text, text_rect)
        self.screen.blit(ip_text, ip_text_rect)

        if self.active and self.activeblink:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (text_rect.topright[0] + 1, text_rect.topright[1], 1, text_rect.height),
            )
