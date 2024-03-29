import subprocess
import time
from typing import List
from src.models.chat_message import ChatMessage, LocalChatMessage
from src.models.game import Game
from src.models.game_user import GameUser
from src.models.user import LocalUser, User
from src.game.server_game import ServerGame as LocalGame
import os
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from sqlalchemy import String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper
from sqlalchemy import and_, or_


class SessionManager:
    _users: List[LocalUser]
    _chat_messages: List[LocalChatMessage]

    def __init__(self):
        self._users = []
        self._chat_messages = []

    @property
    def users(self) -> List[LocalUser]:
        return [user for user in self._users if user.online is True]

    @property
    def users_all(self) -> List[LocalUser]:
        return self._users

    def get_user_by_username(self, username) -> LocalUser | None:
        for user in self._users:
            if user.username == username:
                return user
        return None

    def update_users(self, users: List[LocalUser]):
        for user in users:
            self.update_user(user)

    def update_user(self, user: LocalUser):
        if not self.exists_with_username(user.username):
            self._users.append(user)
            return
        index = next((index for (index, _user) in enumerate(self._users) if _user.username == user.username), None)
        if index is not None:
            self._users[index] = user

    def get_user(self, id: str) -> LocalUser | None:
        for user in self._users:
            if user.id == id:
                return user
        return None

    def get_user_by_dbid(self, id: str) -> LocalUser | None:
        for user in self._users:
            if user.db_id == id:
                return user
        return None

    def exists_with_username(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None

    def exists_with_username_and_online(self, username: str) -> bool:
        user = self.get_user_by_username(username)
        return user is not None and user.online

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
        return len(self.users)

    def get_host(self) -> LocalUser:
        return self._users[0]

    def get_chat_messages(self) -> List[LocalChatMessage]:
        return self._chat_messages

    def add_chat_messages(self, chat_messages):
        for chat_message in chat_messages:
            self._chat_messages.append(chat_message)

    def set_chat_messages(self, chat_messages: List[LocalChatMessage]):
        self._chat_messages = []
        self.add_chat_messages(chat_messages)


class Database:

    def __init__(self):
        self._setup_sqlite3()
        self._engine = create_engine(f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/../../res/database.db", echo=False)

    def _setup_sqlite3(self):
        subprocess.run(['sqlite3', '--init', f'{os.path.dirname(os.path.realpath(__file__))}/../../res/database.sql',  f'{os.path.dirname(os.path.realpath(__file__))}/../../res/database.db', '.quit'])

    @property
    def engine(self):
        return self._engine

    def get_user_by_id(self, user: int) -> User:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(User).where(User.id == user)
            response = session.scalars(statement)
            users = response.fetchall()
            if len(users) == 0:
                return None
            # Use User from db
            db_user = users[0]
        return db_user

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

    def users(self) -> List[User]:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(User)
            response = session.scalars(statement)
            users = response.fetchall()
        return list(users)

    def update_username(self, user: LocalUser):
        update(User).where(User.id == user.db_id).values({
            'username': user.username
        })
        pass

    def chat_message(self, chat_message: ChatMessage) -> ChatMessage:
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(chat_message)
            session.commit()
        return chat_message

    def get_statistics(self, user: int) -> dict:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(GameUser).where(GameUser.user == user)
            response = session.scalars(statement)
            statistics = response.fetchall()
        wins = 0
        loses = 0
        draws = 0
        for statistic in list(statistics):
            if statistic.result == 0:
                draws += 1
            elif statistic.result == 1:
                loses += 1
            elif statistic.result == 2:
                wins += 1
        return {
            'wins': wins,
            'loses': loses,
            'draws': draws
        }

    def get_chat_messages_private(self, user1: int, user2: int) -> List[ChatMessage]:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(ChatMessage).where(
                or_(
                    and_(ChatMessage.to_user == user1, ChatMessage.from_user == user2),
                    and_(ChatMessage.to_user == user2, ChatMessage.from_user == user1)
                )
            )
            response = session.scalars(statement)
            chat_messages = response.fetchall()
        return list(chat_messages)

    def get_chat_messages_global(self) -> List[ChatMessage]:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(ChatMessage).where(ChatMessage.to_user == None)
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
                db_game_user = GameUser(game=db_game.id, user=local_user.db_id, result=None)
                session.add(db_game_user)
            session.commit()
            game._db_id = db_game.id
        return game

    def game_over(self, game: LocalGame):
        with Session(self.engine, expire_on_commit=False) as session:
            # Update the game
            statement = update(Game).where(
                GameUser.game == game.db_id
            ).values({
                'finished': round(time.time()*1000)
            })
            session.execute(statement)
            session.commit()
        return

    def game_over_update_user(self, game: LocalGame, user: LocalUser, result: int):
        with Session(self.engine, expire_on_commit=False) as session:
            # Update the winner
            statement = update(GameUser).where(GameUser.game == game.db_id, GameUser.user == user.db_id).values({
                'result': result
            })
            session.execute(statement)
            session.commit()
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
