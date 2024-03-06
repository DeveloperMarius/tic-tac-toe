from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, BigInteger, String, ForeignKey
from src.models.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    from_user: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"), primary_key=True)
    to_user: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"), primary_key=True)
    message: Mapped[str] = mapped_column(String(1000))
    created: Mapped[int] = mapped_column(BigInteger())

    def __repr__(self) -> str:
        return f"ChatMessage(id={self.id!r})"
