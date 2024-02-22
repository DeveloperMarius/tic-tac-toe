from typing import List
from src.models.user import LocalUser


class SessionManager:
    _users: List[LocalUser]

    def __init__(self):
        self._users = []

    @property
    def users(self) -> List[LocalUser]:
        return self._users

    def add_user(self, user: LocalUser):
        self._users.append(user)

    def get_user(self, id: str) -> LocalUser | None:
        for user in self._users:
            if user.id == id:
                return user
        return None

    def exists_with_username(self, username: str) -> bool:
        print('exists_with_username', username, self._users)
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


class Database:

    def __init__(self):
        pass

    def setup_user(self, user: LocalUser):
        pass

    def save_user(self, user: LocalUser):
        pass
