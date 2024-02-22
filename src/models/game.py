from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, BigInteger
from src.utils import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    started: Mapped[int] = mapped_column(BigInteger())

    def __repr__(self) -> str:
        return f"Game(id={self.id!r})"
