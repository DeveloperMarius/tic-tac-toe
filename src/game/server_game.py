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

    def horizontal_win(self):
        for row in self.board:
            if row == [self.current_player, self.current_player, self.current_player]:
                return True

        return False

    def vertical_win(self):
        for x in range(3):
            if self.board[0][x] == self.current_player and self.board[1][x] == self.current_player and self.board[2][x] == self.current_player:
                return True

        return False

    def diagonal_win(self):
        if self.board[0][0] == self.current_player and self.board[1][1] == self.current_player and self.board[2][2] == self.current_player:
            return True

        if self.board[0][2] == self.current_player and self.board[1][1] == self.current_player and self.board[2][0] == self.current_player:
            return True

        return False

    def check_winner(self) -> bool:
        if self.horizontal_win():
            return True

        if self.vertical_win():
            return True

        if self.diagonal_win():
            return True

        return False

    def is_draw(self) -> bool:
        for row in self.board:
            for field in row:
                if field is None:
                    return False

        return True

    def check_game_over(self) -> bool:
        return self.check_winner() or self.is_draw()
