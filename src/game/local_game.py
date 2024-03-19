import random

from src.game.config import ClientConfig
from src.game.events import Event, EventType
from src.game.network import NetworkClient
from src.windows.components.tictactoe_field import FieldRect


class LocalGame:

    _db_id: int | None

    def __init__(self, player_ids) -> None:
        # None = Nothing
        # 1 = X
        # 2 = O
        self.winner = 0
        self._players = player_ids

    def handle_turn(self, index: int, fields: list[FieldRect]):
        NetworkClient.first().send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': index % 3,
            'y': index // 3
        }))

        return fields

    @property
    def db_id(self) -> int:
        return self._db_id
