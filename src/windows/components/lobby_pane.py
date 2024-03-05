import pygame
from .base_component import BaseComponent


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

        self.host_name = "A"
        self.player_name = ""
        self.host_ready = True
        self.player_ready = False

    @property
    def host_name(self):
        """Return host name"""
        return self._host_name

    @host_name.setter
    def host_name(self, value):
        """Set host name"""
        self._host_name = value

    @property
    def player_name(self):
        """Return player name"""
        return self._player_name

    @player_name.setter
    def player_name(self, value):
        """Set player name"""
        self._player_name = value

    @property
    def host_ready(self):
        """Return if host is ready"""
        return self._host_ready

    @host_ready.setter
    def host_ready(self, value):
        """Set if host is ready"""
        self._host_ready = value

    @property
    def player_ready(self):
        """Return if player is ready"""
        return self._player_ready

    @player_ready.setter
    def player_ready(self, value):
        """Set if player is ready"""
        self._player_ready = value

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
            self.background_ready_color if self.host_ready else self.background_color,
            host_box,
            border_radius=15,
        )
        # Draw host text
        host_text = self.font.render(f"{self.host_name} (HOST)", True, (255, 255, 255))
        host_text_rect = host_text.get_rect(
            topleft=(self.x + self.padding, self.y + self.padding)
        )
        self.screen.blit(host_text, host_text_rect)
        # Draw ready text (if applicable)
        if self.host_ready:
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
            self.background_ready_color if self.player_ready else self.background_color,
            player_box,
            border_radius=15,
        )
        # Draw player text
        player_text = self.font.render(
            self.player_name if self.player_name else "Waiting for player to join ...",
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
        if self.player_ready:
            ready_text = self.font.render("Ready", True, (255, 255, 255))
            ready_text_rect = ready_text.get_rect(
                topright=(
                    self.x + self.width - self.padding,
                    self.y + self.font_size + self.padding * 3 + self.padding,
                )
            )
            self.screen.blit(ready_text, ready_text_rect)
