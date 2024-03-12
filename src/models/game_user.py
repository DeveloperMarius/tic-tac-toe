from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, Boolean
from src.models.base import Base


class GameUser(Base):
    __tablename__ = "game_users"

    game: Mapped[int] = mapped_column(Integer(), ForeignKey("games.id"), primary_key=True)
    user: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"), primary_key=True)
    won: Mapped[bool] = mapped_column(Boolean())

    def __repr__(self) -> str:
        return f"GameUser(game={self.game!r}, user={self.user!r})"
