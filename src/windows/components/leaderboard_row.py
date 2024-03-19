import pygame


class LeaderboardRow:
    def __init__(
        self, screen, index, player_stats, x, y, width, height, color=(20, 33, 61)
    ) -> None:
        self.screen = screen
        self.index = index
        self.player_stats = player_stats
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        if self.player_stats is None:
            return

        self.rect = pygame.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width * 0.75, self.height),
            border_radius=10,
        )
        pygame.font.init()
        font = pygame.font.SysFont("Comic Sans MS", 36)
        text = font.render(
            (
                (f"{self.index}. {self.player_stats['username']}")
                if self.index != 0
                else "Username"
            ),
            True,
            (255, 255, 255),
        )
        text_rect = text.get_rect(
            center=(self.x + self.width * 0.75 / 2, self.y + self.height / 2)
        )
        self.screen.blit(text, text_rect)

        for i, value in enumerate(["wins", "loses", "draws"]):
            rect_w = self.width * 0.25 / 3 - 30
            self.rect = pygame.draw.rect(
                self.screen,
                (0, 255, 0) if i == 0 else (255, 0, 0) if i == 1 else (0, 0, 255),
                (
                    self.x + self.width * 0.75 + rect_w * i + 10 * (i + 1),
                    self.y,
                    rect_w,
                    self.height,
                ),
                border_radius=10,
            )
            text = font.render(
                str(self.player_stats[value]),
                True,
                (255, 255, 255),
            )
            text_rect = text.get_rect(
                center=(
                    self.x + self.width * 0.75 + rect_w * i + rect_w / 2 + 10 * (i + 1),
                    self.y + self.height / 2,
                )
            )
            self.screen.blit(text, text_rect)
