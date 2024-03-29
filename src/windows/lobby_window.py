import pygame

from .window_manager import Window, WindowManager
from .components.button import Button
from .components.chat_pane import ChatPane
from .components.lobby_pane import LobbyPane
from ..game.config import Clients
from ..game.events import Event, EventType
from ..game.network import NetworkServer, NetworkClient


class LobbyWindow(Window):
    def __init__(self):
        super().__init__()
        self.lobby_pane = LobbyPane(
            self.screen,
            0 + 0.05 * self.width,
            0 + self.height * 0.35,
            0.55 * self.width,
            self.height * 0.18,
        )
        self.chat_pane = ChatPane(
            self.screen,
            0.675 * self.width,
            0 + self.height * 0.1,
            0.25 * self.width,
            self.height * 0.8,
        )

        button_ready = Button(
            self.screen,
            "Ready",
            self.lobby_pane.x,
            self.lobby_pane.y + self.lobby_pane.height + self.height * 0.02,
            self.lobby_pane.width * 0.49,
            self.height * 0.075,
        )

        self.leaving = False
        button_leave = Button(
            self.screen,
            "Leave",
            self.lobby_pane.x + self.lobby_pane.width * 0.51,
            self.lobby_pane.y + self.lobby_pane.height + self.height * 0.02,
            self.lobby_pane.width * 0.49,
            self.height * 0.075,
        )

        button_leaderboard = Button(
            self.screen,
            "Leaderboard",
            self.lobby_pane.x,
            self.lobby_pane.y
            + self.lobby_pane.height
            + button_leave.height
            + self.height * 0.04,
            self.lobby_pane.width,
            self.height * 0.075,
        )

        self.buttons = [button_ready, button_leave, button_leaderboard]

    def draw(self, _: pygame.Surface):
        self.lobby_pane.draw()
        self.chat_pane.draw()

        self.draw_buttons()

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def handleEvent(self, event):
        self.chat_pane.handleEvent(event)
        for button in self.buttons:
            match button.text:
                case "Ready":
                    if event.type == pygame.MOUSEBUTTONUP:
                        if button.rect.collidepoint(event.pos):
                            print("Ready")
                            print(Clients.first().get_user().ready)
                            print(Clients.first().get_sessionmanager().users[0].ready)
                            NetworkClient.first().send(
                                Event(
                                    EventType.LOBBY_READY,
                                    {"ready": not Clients.first().get_user().ready},
                                )
                            )

                case "Leave":
                    if event.type == pygame.MOUSEBUTTONUP and not self.leaving:
                        if button.rect.collidepoint(event.pos):
                            print("Leave")

                            from .main_menu_window import MainMenuWindow

                            try:
                                self.leaving = True
                                NetworkClient.first().disconnect()
                                if NetworkServer.get_instance().running:
                                    NetworkServer.get_instance().shutdown()
                            except Exception:
                                print("Error leaving")
                            finally:
                                self.leaving = False
                                WindowManager.get_instance().activeWindow = (
                                    MainMenuWindow()
                                )

                case "Leaderboard":
                    if event.type == pygame.MOUSEBUTTONUP:
                        if button.rect.collidepoint(event.pos):
                            from .leaderboard_window import LeaderboardWindow

                            WindowManager.get_instance().activeWindow = (
                                LeaderboardWindow()
                            )
