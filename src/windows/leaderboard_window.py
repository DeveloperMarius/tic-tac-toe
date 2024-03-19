import pygame


from .components.menu_title import MenuTitle
from .window_manager import Window, WindowManager
from .components.button import Button
from .components.leaderboard_row import LeaderboardRow


class LeaderboardWindow(Window):
    def __init__(self):
        super().__init__()

        self.menu_width = 0.8 * self.width
        self.menu_height = 0.75 * self.height

        self.menu_title = MenuTitle(
            title="Leaderboard",
            x=self.mid_x,
            y=self.mid_y - self.menu_height / 2 + self.mid_y / 6,
        )

        button_width = self.menu_width
        button_height = 0.1 * self.menu_height
        button_margin = 0.025 * self.menu_height

        # TODO: Get leaderboard
        self.leaderboard = [
            {"username": "test", "wins": 2, "loses": 3, "draws": 5},
            {"username": "test2", "wins": 3, "loses": 2, "draws": 5},
            {"username": "test3", "wins": 3, "loses": 2, "draws": 6},
        ]

        self.leaderboard.sort(key=lambda x: (-x["wins"], x["loses"], -x["draws"]))

        self.leaderboard.insert(
            0,
            {
                "username": "USERNAME",
                "wins": "W",
                "loses": "L",
                "draws": "D",
            },
        )

        self.leaderboard_rows = [
            LeaderboardRow(
                screen=self.screen,
                index=i,
                player_stats=player_stats,
                x=self.width * 0.1,
                y=self.mid_y * 1.3
                - self.menu_height / 2
                + i * button_height
                + button_margin * (i + 1)
                + 10,
                width=button_width,
                height=button_height,
            )
            for i, player_stats in enumerate(self.leaderboard)
        ]

        self.close_button = Button(
            screen=self.screen,
            text="X",
            x=self.width - 40,
            y=20,
            width=20,
            height=20,
        )

    def handleEvent(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if not self.close_button.rect.collidepoint(event.pos):
            return
        if self.close_button.text == "X":
            from .lobby_window import LobbyWindow

            WindowManager.get_instance().activeWindow = LobbyWindow()

    def draw(self, screen):
        for row in self.leaderboard_rows:
            row.draw()

        self.close_button.draw()
        self.menu_title.draw(screen)
