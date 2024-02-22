from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer
from src.utils import Base


class GameUser(Base):
    __tablename__ = "game_users"

    game: Mapped[int] = mapped_column(Integer(), ForeignKey("games.id"), primary_key=True)
    user: Mapped[str] = mapped_column(String(), ForeignKey("users.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"Game(game={self.game!r}, user={self.user!r})"
