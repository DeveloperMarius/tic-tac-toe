
class LocalUser:

    _id: str
    _username: str
    _admin: bool = False

    def __init__(self, id: str, username: str, admin: bool = False):
        self._id = id
        self._username = username
        self._admin = admin

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def is_admin(self) -> bool:
        return self._admin
