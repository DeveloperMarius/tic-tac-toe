import pygame

from .input import Input

from .base_component import BaseComponent
from ...game.config import ClientConfig
from ...game.events import EventType, Event
from ...game.network import NetworkClient


class ChatPane(BaseComponent):
    """Component for displaying a chat log"""

    def __init__(self, screen: pygame.Surface, x, y, width, height):
        """Initialize chat pane component"""
        super().__init__()

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.background_color = (20, 33, 61)
        self.text_color = (255, 255, 255)
        self.font_size = 20
        self.font = pygame.font.SysFont("Helvetica", self.font_size)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.chat_log: list = []
        self.scroll_offset = 0
        self.mouse_pos = (0, 0)

        self.input = Input(
            self.screen,
            "",
            self.x + 10,
            self.y + self.height - self.height * 0.08,
            10,
            self.width - 20,
            self.height * 0.07,
            (7, 12, 23),
        )

    @property
    def chat_log(self):
        return self._chat_log

    @chat_log.setter
    def chat_log(self, value):
        """Set chat log"""
        self.scroll_offset = 0
        self._chat_log = value

    def draw(self):
        """Draw chat pane component"""
        self.screen.fill(self.background_color, self.rect)

        for i, chat_message in enumerate(reversed(ClientConfig.get_sessionmanager().get_chat_messages())):
            if (
                self.y
                + self.height
                - self.height * 0.10
                - (i + 1) * self.font_size
                - self.scroll_offset
            ) < self.y + self.height * 0.07:
                continue

            from_user_obj = ClientConfig.get_sessionmanager().get_user(chat_message.from_user)
            rendered_message = self.font.render(
                f"{from_user_obj.username if from_user_obj is not None else chat_message.from_user_username}: {chat_message.message}",
                True,
                self.text_color,
            )
            message_rect = rendered_message.get_rect(
                topleft=(
                    self.x + self.width * 0.02,
                    self.y
                    + self.height
                    - self.height * 0.10
                    - (i + 1) * self.font_size
                    - self.scroll_offset,
                )
            )
            self.screen.blit(rendered_message, message_rect)

        pygame.draw.rect(
            self.screen,
            self.background_color,
            (
                self.x,
                self.input.y - 10,
                self.width,
                self.input.height + 20,
            ),
        )

        self.input.draw()

        title_font = pygame.font.SysFont("Helvetica", 36, True)
        rendered_name = title_font.render(
            "Chat",
            True,
            self.text_color,
        )
        name_rect = rendered_name.get_rect(
            center=(
                self.x + self.width * 0.5,
                self.y + self.height * 0.05,
            )
        )

        self.screen.blit(rendered_name, name_rect)

        pygame.draw.rect(
            self.screen,
            self.background_color,
            (
                self.x,
                self.y + self.height * 0.055 + self.font_size / 2,
                self.width,
                self.font_size,
            ),
        )

    def handleEvent(self, event):
        """Handle chat pane component events"""

        if text := self.input.handle_events(event):
            NetworkClient.get_instance().send(Event(EventType.CHAT_MESSAGE, {
                'chat_message': {
                    'to_user': None,
                    'from_user': ClientConfig.get_sessionmanager().get_user_by_username(ClientConfig.get_username()),
                    'message': text
                }
            }))
            self.input.text = ""

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return

        if event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos):
            self.mouse_pos = event.pos

        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(self.mouse_pos):
            self.scroll_offset += event.y * 5
            self.scroll_offset = max(0, self.scroll_offset)
