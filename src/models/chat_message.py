from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, BigInteger, String, ForeignKey
from src.models.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    from_user: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"), primary_key=True)
    to_user: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"), primary_key=True, nullable=True)
    message: Mapped[str] = mapped_column(String(1000))
    created: Mapped[int] = mapped_column(BigInteger())

    def __repr__(self) -> str:
        return f"ChatMessage(id={self.id!r})"


class LocalChatMessage:

    _db_id: int | None
    _from_user: str | None
    _to_user: str = None
    _message: str
    _created: int
    _from_user_username: str | None = None

    def __init__(self, from_user: str | None, message: str, created: int, to_user: str | None = None, db_id: int | None = None, from_user_username: str | None = None):
        self._from_user = from_user
        self._to_user = to_user
        self._message = message
        self._created = created
        self._db_id = db_id
        self._from_user_username = from_user_username

    @property
    def db_id(self) -> int:
        return self._db_id

    @property
    def from_user(self) -> str | None:
        return self._from_user

    @property
    def to_user(self) -> str | None:
        return self._to_user

    @property
    def message(self) -> str:
        return self._message

    @property
    def created(self) -> int:
        return self._created

    @property
    def from_user_username(self) -> str | None:
        return self._from_user_username
