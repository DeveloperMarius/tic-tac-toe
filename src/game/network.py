import time

import socketio
import eventlet


class NetworkClient:

    _sio: socketio.Client

    def __init__(self):
        self._sio = socketio.Client()

    def __enter__(self):
        self._connect()
        return self

    def _connect(self):
        self.call_backs()
        self._sio.connect('http://localhost:5000')

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
        def connect(sid, environ):
            print('connect ', sid)

        @self._sio.event
        def my_message(sid, data):
            print('message ', sid, data)

        @self._sio.event
        def disconnect(sid):
            print('disconnect ', sid)
