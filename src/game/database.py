import subprocess
import time
from typing import List

from src.models.chat_message import ChatMessage, LocalChatMessage
from src.models.game import Game
from src.models.game_user import GameUser
from src.models.user import LocalUser, User
from src.game.game import Game as LocalGame
import os
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from sqlalchemy import String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper


class SessionManager:
    _users: List[LocalUser]

    def __init__(self):
        self._users = []

    @property
    def users(self) -> List[LocalUser]:
        return self._users

    def add_user(self, user: LocalUser):
        self._users.append(user)

    def update_user(self, user: LocalUser):
        index = next((index for (index, _user) in enumerate(self._users) if _user.id == user.id), None)
        self._users[index] = user

    def get_user(self, id: str) -> LocalUser | None:
        for user in self._users:
            if user.id == id:
                return user
        return None

    def exists_with_username(self, username: str) -> bool:
        for user in self._users:
            if user.username == username:
                return True
        return False

    def exists_with_id(self, id: str) -> bool:
        for user in self._users:
            if user.id == id:
                return True
        return False

    def remove_user(self, id: str):
        index = next((index for (index, user) in enumerate(self._users) if user.id == id), None)
        if index is not None:
            self._users.pop(index)
        return index is not None

    def user_count(self) -> int:
        return len(self._users)

    def set_users(self, users: List[LocalUser]):
        self._users = users


class Database:

    def __init__(self):
        self._setup_sqlite3()
        self._engine = create_engine(f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/../../res/database.db", echo=False)

    def _setup_sqlite3(self):
        subprocess.run(['sqlite3', '--init', f'{os.path.dirname(os.path.realpath(__file__))}/../../res/database.sql',  f'{os.path.dirname(os.path.realpath(__file__))}/../../res/database.db', '.quit'])

    @property
    def engine(self):
        return self._engine

    def get_user(self, user: LocalUser):
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(User).where(User.username == user.username)
            response = session.scalars(statement)
            users = response.fetchall()
            if len(users) == 0:
                # Create User in db
                db_user = User(
                    username=user.username
                )
                session.add(db_user)
                session.commit()
            else:
                # Use User from db
                db_user = users[0]
        return db_user

    def save_user(self, user: LocalUser):
        # update(User).where(User.username == user.username).values()
        pass

    def chat_message(self, chat_message: LocalChatMessage) -> ChatMessage:
        with Session(self.engine, expire_on_commit=False) as session:
            db_chat_message = ChatMessage(
                from_user=chat_message.from_user,
                to_user=chat_message.to_user,
                message=chat_message.message,
                created=chat_message.created
            )
            session.add(db_chat_message)
            session.commit()
        return db_chat_message

    def get_chat_messages_private(self, user1: int, user2: int) -> List[ChatMessage]:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(ChatMessage).where(
                (ChatMessage.to_user == user1 and ChatMessage.from_user == user2)
                or
                (ChatMessage.to_user == user2 and ChatMessage.from_user == user1)
            )
            response = session.scalars(statement)
            chat_messages = response.fetchall()
        return list(chat_messages)

    def get_chat_messages_global(self) -> List[ChatMessage]:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(ChatMessage).where(ChatMessage.to_user is None)
            response = session.scalars(statement)
            chat_messages = response.fetchall()
        return list(chat_messages)

    def get_game(self, game: LocalGame) -> Game | None:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(Game).where(Game.id == game.db_id)
            response = session.scalars(statement)
            games = response.fetchall()
            if len(games) == 0:
                return None
            return games[0]

    def game_start(self, game: LocalGame, local_users: List[LocalUser]) -> LocalGame:
        with Session(self.engine, expire_on_commit=False) as session:
            game.started = round(time.time()*1000)
            db_game = Game(started=game.started, finished=None)
            session.add(db_game)
            session.commit()
            for player in game.players:
                local_user = None
                for _local_user in local_users:
                    if _local_user.id == player:
                        local_user = _local_user
                        break
                db_game_user = GameUser(game=db_game.id, user=local_user.db_id, won=False)
                session.add(db_game_user)
        return game

    def game_over(self, game: LocalGame, winner: LocalUser):
        with Session(self.engine, expire_on_commit=False) as session:
            # Update the game
            statement = update(Game).where(
                GameUser.game == game.db_id
            ).values({
                'finished': round(time.time()*1000)
            })
            session.execute(statement)
            # Update the winner
            statement2 = update(GameUser).where(
                GameUser.game == game.db_id and
                GameUser.user == winner.db_id
            ).values({
                'won': True
            })
            session.execute(statement2)
        return


class EventHandler:

    @staticmethod
    @listens_for(Mapper, "before_insert")
    def receive_before_insert(mapper, connection, target):
        table = target.__table__
        EventHandler._validate(target.__dict__, table.columns)

    @staticmethod
    @listens_for(Mapper, "before_update")
    def receive_before_update(mapper, connection, target):
        table = target.__table__
        EventHandler._validate(target.__dict__, table.columns)

    @staticmethod
    def _validate(data, columns):
        for column in columns:
            if column.name not in data:
                continue
            value = data[column.name]
            if isinstance(column.type, String):
                length = column.type.length
                if value is None:
                    if not column.nullable:
                        raise ValueError(f"{column.name} cannot be null.")
                    continue
                if len(value) > length:
                    raise ValueError(f"{column.name} is to long. {len(value)} > {length}")
