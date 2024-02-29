from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer

from src.utils import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"


class LocalUser:

    _id: str
    _db_id: int | None
    _username: str
    _admin: bool = False
    _ready: bool = False

    def __init__(self, id: str, username: str, admin: bool = False, db_id: int | None = None):
        self._id = id
        self._username = username
        self._admin = admin
        self._db_id = db_id

    @property
    def id(self) -> str:
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

    def __str__(self) -> str:
        return f"User(id={self.id!r}, db_id={self.db_id!r})"
