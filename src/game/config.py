from typing import List

from src.game.database import Database, SessionManager
from src.game.events import EventManager
from src.game.server_game import ServerGame
from src.models.user import LocalUser


class ClientConfig:

    _eventmanager_instance: EventManager | None = None
    _sessionmanager_instance: SessionManager | None = None
    _username: str | None = None

    def set_username(self, username: str):
        self._username = username

    def get_username(self) -> str:
        return self._username

    def get_user(self) -> LocalUser | None:
        return self.get_sessionmanager().get_user_by_username(self.get_username())

    def get_eventmanager(self) -> EventManager:
        if self._eventmanager_instance is None:
            self._eventmanager_instance = EventManager()
        return self._eventmanager_instance

    def get_sessionmanager(self) -> SessionManager:
        if self._sessionmanager_instance is None:
            self._sessionmanager_instance = SessionManager()
        return self._sessionmanager_instance


class Clients:
    _clients: List[ClientConfig] = []

    @staticmethod
    def first() -> ClientConfig:
        if len(Clients._clients) == 0:
            Clients.add_client()
        return Clients._clients[0]

    @staticmethod
    def second() -> ClientConfig:
        if len(Clients._clients) == 1:
            Clients.add_client()
        return Clients._clients[1]

    @staticmethod
    def add_client():
        config = ClientConfig()
        Clients._clients.append(config)
        return config

    @staticmethod
    def clients() -> List[ClientConfig] | None:
        return Clients._clients


class ServerConfig:

    lobby_max_players = 2
    _database_instance: Database | None = None
    _sessionmanager_instance: Database | None = None
    _game_instance: ServerGame | None = None

    @staticmethod
    def reset():
        ServerConfig._database_instance = None
        ServerConfig._sessionmanager_instance = None
        ServerConfig._game_instance = None

    @staticmethod
    def get_database() -> Database:
        if ServerConfig._database_instance is None:
            ServerConfig._database_instance = Database()
        return ServerConfig._database_instance

    @staticmethod
    def get_sessionmanager() -> SessionManager:
        if ServerConfig._sessionmanager_instance is None:
            ServerConfig._sessionmanager_instance = SessionManager()
        return ServerConfig._sessionmanager_instance

    @staticmethod
    def get_game() -> ServerGame | None:
        return ServerConfig._game_instance

    @staticmethod
    def create_game(player_ids: List[str]) -> ServerGame:
        ServerConfig._game_instance = ServerGame(player_ids)
        return ServerConfig.get_game()

    @staticmethod
    def delete_game():
        ServerConfig._game_instance = None
