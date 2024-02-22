from src.game.database import Database, SessionManager
from src.game.events import EventManager


class ClientConfig:

    _eventmanager_instance: EventManager | None = None
    _sessionmanager_instance: Database | None = None

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
