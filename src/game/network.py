from typing import List
import socketio
import eventlet
from src.models.user import LocalUser
from src.game.config import Config


class NetworkClient:

    _sio: socketio.Client
    _username: str

    def __init__(self, username):
        self._sio = socketio.Client()
        self._username = username

    def __enter__(self):
        self._connect()
        return self

    @property
    def username(self):
        return self._username

    def _connect(self):
        self.call_backs()
        self._sio.connect('http://localhost:5000', {
            'username': self.username
        }, 'authtoken')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sio.disconnect()

    def call_backs(self):
        @self._sio.event
        def connect():
            print('connection established')

        @self._sio.event
        def my_message(data):
            print('message received with ', data)
            self._sio.emit('my_response', {'response': 'my response'})

        @self._sio.event
        def disconnect():
            print('disconnected from server')

    def send(self, event, data):
        self._sio.emit(event, data)


class NetworkServer:

    _sio: socketio.Server

    def __init__(self):
        self._sio = socketio.Server()
        self.call_backs()
        self.app = socketio.WSGIApp(self._sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'index.html'}
        })

    def __enter__(self):
        self.start_server()
        return self._sio

    def start_server(self):
        eventlet.wsgi.server(eventlet.listen(('', 5000)), self.app)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self._sio.shutdown()

    def call_backs(self):
        @self._sio.event
        def connect(sid, headers, auth):
            print('connect ', sid, headers, auth)
            username = headers['HTTP_USERNAME']

            # Check if user is already playing
            if Config.get_sessionmanager().exists_with_username(username):
                return False

            # Apply user limit
            if Config.get_sessionmanager().user_count() >= Config.lobby_max_players:
                return False

            # Add user to local user cache
            Config.get_database().setup_user(LocalUser(sid, username))

            return True

        @self._sio.event
        def my_message(sid, data):
            print('message ', sid, data)

        @self._sio.event
        def disconnect(sid):
            print('disconnect ', sid)
            # Check if user is in local user cache
            if not Config.get_sessionmanager().exists_with_id(sid):
                return False

            # Save and Remove user from local user cache
            user = Config.get_sessionmanager().get_user(sid)
            Config.get_database().save_user(user)
            Config.get_sessionmanager().remove_user(sid)

            return True
