import pygame
from .base_component import BaseComponent
from ...game.config import Clients


class LobbyPane(BaseComponent):
    """Lobby pane component"""

    def __init__(
        self,
        screen,
        x,
        y,
        width,
        height,
    ):
        super().__init__()

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.background_color = (20, 33, 61)
        self.background_ready_color = (252, 163, 17)
        self.text_color = (255, 255, 255)
        self.font_size = 24
        self.padding = 15
        self.font = pygame.font.SysFont("Helvetica", self.font_size)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """Draw lobby pane component"""
        # Draw Title
        title_font = pygame.font.SysFont("Helvetica", 48, True)
        title_text = title_font.render("Lobby", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(
            center=(self.x + self.width / 2, self.y - 54)
        )
        self.screen.blit(title_text, title_text_rect)

        # Draw host box
        host_box = pygame.Rect(
            self.x, self.y, self.width, self.font_size + self.padding * 2
        )
        pygame.draw.rect(
            self.screen,
            self.background_ready_color if len(Clients.first().get_sessionmanager().users) > 0 and Clients.first().get_sessionmanager().users[0].ready else self.background_color,
            host_box,
            border_radius=15,
        )
        # Draw host text
        host_text = self.font.render(f"{Clients.first().get_sessionmanager().users[0].username if len(Clients.first().get_sessionmanager().users) > 0 else 'Loading...'}", True, (255, 255, 255))
        host_text_rect = host_text.get_rect(
            topleft=(self.x + self.padding, self.y + self.padding)
        )
        self.screen.blit(host_text, host_text_rect)
        # Draw ready text (if applicable)
        if len(Clients.first().get_sessionmanager().users) > 0 and Clients.first().get_sessionmanager().users[0].ready:
            ready_text = self.font.render("Ready", True, (255, 255, 255))
            ready_text_rect = ready_text.get_rect(
                topright=(self.x + self.width - self.padding, self.y + self.padding)
            )
            self.screen.blit(ready_text, ready_text_rect)

        # Draw player box
        player_box = pygame.Rect(
            self.x,
            self.y + self.font_size + self.padding * 3,
            self.width,
            self.font_size + self.padding * 2,
        )
        pygame.draw.rect(
            self.screen,
            self.background_ready_color if len(Clients.first().get_sessionmanager().users) > 1 and Clients.first().get_sessionmanager().users[1].ready else self.background_color,
            player_box,
            border_radius=15,
        )
        # Draw player text
        player_text = self.font.render(
            f'{Clients.first().get_sessionmanager().users[1].username}' if len(
                Clients.first().get_sessionmanager().users) > 1 else 'Waiting for player to join ...',
            True,
            (255, 255, 255),
        )
        player_text_rect = player_text.get_rect(
            topleft=(
                self.x + self.padding,
                self.y + self.font_size + self.padding * 3 + self.padding,
            )
        )
        self.screen.blit(player_text, player_text_rect)
        # Draw ready text (if applicable)
        if len(Clients.first().get_sessionmanager().users) > 1 and Clients.first().get_sessionmanager().users[1].ready:
            ready_text = self.font.render("Ready", True, (255, 255, 255))
            ready_text_rect = ready_text.get_rect(
                topright=(
                    self.x + self.width - self.padding,
                    self.y + self.font_size + self.padding * 3 + self.padding,
                )
            )
            self.screen.blit(ready_text, ready_text_rect)
