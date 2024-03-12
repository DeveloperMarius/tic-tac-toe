from typing import List

from src.game.database import Database, SessionManager
from src.game.events import EventManager
from src.game.server_game import ServerGame


class ClientConfig:

    _eventmanager_instance: EventManager | None = None
    _sessionmanager_instance: Database | None = None
    _username: str | None = None

    @staticmethod
    def set_username(username: str):
        ClientConfig._username = username

    @staticmethod
    def get_username() -> str:
        return ClientConfig._username

    @staticmethod
    def get_eventmanager() -> EventManager:
        if ClientConfig._eventmanager_instance is None:
            ClientConfig._eventmanager_instance = EventManager()
        return ClientConfig._eventmanager_instance

    @staticmethod
    def get_sessionmanager() -> SessionManager:
        if ClientConfig._sessionmanager_instance is None:
            ClientConfig._sessionmanager_instance = SessionManager()
        return ClientConfig._sessionmanager_instance


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
