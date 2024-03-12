import random


class ServerGame:

    _db_id: int | None
    _current_player: str | None = None

    def __init__(self, player_ids) -> None:
        # None = Nothing
        # 1 = X
        # 2 = O
        self.winner = 0
        self._players = player_ids
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def handle_turn(self, x: int, y: int) -> bool:
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
    def db_id(self) -> int:
        return self._db_id

    @property
    def current_player(self) -> str:
        return self._current_player

    @property
    def players(self) -> list[str]:
        return self._players

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
