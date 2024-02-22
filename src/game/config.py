from src.game.database import Database, SessionManager


class Config:

    lobby_max_players = 2
    _database_instance: Database | None = None
    _sessionmanager_instance: Database | None = None

    @staticmethod
    def get_database() -> Database:
        if Config._database_instance is None:
            Config._database_instance = Database()
        return Config._database_instance

    @staticmethod
    def get_sessionmanager() -> SessionManager:
        if Config._sessionmanager_instance is None:
            Config._sessionmanager_instance = SessionManager()
        return Config._sessionmanager_instance
