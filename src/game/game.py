import random
from src.windows.components.tictactoe_field import FieldRect


class Game:

    _current_player: str | None = None

    def __init__(self, player_ids) -> None:
        # None = Nothing
        # 1 = X
        # 2 = O
        self.winner = 0
        self.players = player_ids
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def move(self, x: int, y: int) -> bool:
        if self.board[y][x] is not None:
            return False

        self.board[y][x] = self.current_player
        return True

    def next_player_to_move(self) -> str:
        if self._current_player is None:
            self._current_player = random.choice(self.players)
            return self._current_player

        last_player = self._current_player
        self._current_player = random.choice([player for player in self.players if player != last_player])
        return self._current_player

    @property
    def current_player(self) -> str:
        return self._current_player

    def handle_turn(self, index: int, fields: list[FieldRect]):
        # Check if the field is already checked
        if self.board[index // 3][index % 3] != 0:
            return

        # Update the field
        fields[index].checked = self.player
        self.board[index // 3][index % 3] = self.player

        # Change the player
        self.player = 1 if self.player == 2 else 2

        # Check for winner
        self.check_winner()

        return fields

    def hoizontal_win(self):
        for row in self.board:
            symbol = row[0]
            if row == [symbol, symbol, symbol]:
                return True

        return False

    def vertical_win(self):
        list(zip(self.board[::-1]))

    def diagonal_win(self):
        pass

    def check_winner(self) -> bool:
        if self.hoizontal_win():
            return True

        if self.vertical_win():
            return True

        if self.diagonal_win():
            return True

        return False
