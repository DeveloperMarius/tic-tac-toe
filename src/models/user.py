from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer
from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"


class LocalUser:

    _id: str | None
    _db_id: int | None
    _username: str
    _admin: bool = False
    _online: bool = False
    _ready: bool = False
    _game_symbol: int | None = None
    # {'wins': wins, 'loses': loses, 'draws': draws}
    _statistics: dict | None = None

    def __init__(self, id: str | None, username: str, admin: bool = False, db_id: int | None = None, ready: bool = False, game_symbol: int | None = None, statistics: dict | None = None, online: bool = False):
        self._id = id
        self._username = username
        self._admin = admin
        self._db_id = db_id
        self._ready = ready
        self._game_symbol = game_symbol
        self._statistics = statistics
        self._online = online

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def db_id(self) -> int:
        return self._db_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def is_admin(self) -> bool:
        return self._admin

    @db_id.setter
    def db_id(self, value):
        self._db_id = value

    @property
    def ready(self) -> bool:
        return self._ready

    @ready.setter
    def ready(self, value: bool):
        self._ready = value

    @property
    def game_symbol(self) -> int | None:
        return self._game_symbol

    @game_symbol.setter
    def game_symbol(self, value: int | None):
        self._game_symbol = value

    @property
    def statistics(self) -> dict | None:
        return self._statistics

    @statistics.setter
    def statistics(self, value: dict | None):
        self._statistics = value

    @property
    def online(self) -> bool:
        return self._online

    @online.setter
    def online(self, value: bool):
        self._online = value

    def __str__(self) -> str:
        return f"User(id={self.id!r}, db_id={self.db_id!r})"
