import socketio
import eventlet
import multiprocessing
from src.models.chat_message import LocalChatMessage
from src.models.user import LocalUser
from src.game.config import ClientConfig, ServerConfig
from src.game.events import Event, EventType
import json
from src.utils.json_encoder import ModelEncoder
from threading import Thread
import time


class NetworkClient:

    _sio: socketio.Client
    _username: str

    def __init__(self, username):
        self._sio = socketio.Client()
        self._username = username

    def __enter__(self):
        self.connect()
        return self

    @property
    def username(self):
        return self._username

    def connect(self):
        self.call_backs()
        self._register_default_events()
        self._sio.connect('http://localhost:5000', {
            'username': self.username
        }, 'authtoken')
        self.send(Event(EventType.SYNC))

    def _register_default_events(self):
        ClientConfig.get_eventmanager().clear_events()
        ClientConfig.get_eventmanager().on(EventType.USER_JOIN, lambda event: ClientConfig.get_sessionmanager().add_user(event.data['user']))
        ClientConfig.get_eventmanager().on(EventType.USER_LEAVE, lambda event: ClientConfig.get_sessionmanager().remove_user(event.data['user'].id))
        ClientConfig.get_eventmanager().on(EventType.SYNC, lambda event: self._event_sync(event))

    def _event_sync(self, event):
        users = [LocalUser(**user) for user in event.data['users']]
        ClientConfig.get_sessionmanager().set_users(users)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sio.disconnect()

    def call_backs(self):
        @self._sio.event
        def connect():
            print('connection established')

        @self._sio.on('*')
        def any_event(event, data):
            print('message received with ', event, data)
            parsed_data = json.loads(data)
            if 'user' in parsed_data:
                parsed_data['user'] = LocalUser(**parsed_data['user'])
            if 'chat_messages' in parsed_data:
                chat_messages = []
                for chat_message in parsed_data['chat_messages']:
                    chat_messages.append(LocalChatMessage(**chat_message))
                parsed_data['chat_messages'] = chat_messages
            event_type = EventType(event)
            ClientConfig.get_eventmanager().trigger(Event(event_type, parsed_data))

        @self._sio.event
        def disconnect():
            print('disconnected from server')

    def send(self, event: Event):
        self._sio.emit(event.type.value, event.data)

    def send_request(self, event_type: EventType):
        self._sio.emit(event_type.value, {})


class NetworkServer:

    _sio: socketio.Server

    def __init__(self):
        self._sio = socketio.Server()
        self.call_backs()
        self.app = socketio.WSGIApp(self._sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'index.html'}
        })
        self._thread = multiprocessing.Process(target=self._start_server, args=())
        # self._thread = Thread(target=self._start_server)

    def __enter__(self):
        self.start_server()
        return self._sio

    def start_server(self):
        self._thread.start()
        time.sleep(5)

    def _start_server(self):
        eventlet.wsgi.server(eventlet.listen(('', 5000)), self.app)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self._thread.terminate()
        self._sio.shutdown()

    def send(self, event: Event, to=None, skip_sid=None):
        self._sio.emit(event.type.value, json.dumps(event.data, cls=ModelEncoder), to=to, skip_sid=skip_sid)

    def call_backs(self):
        @self._sio.event
        def connect(sid, headers, auth):
            print('connect ', sid, headers, auth)
            username = headers['HTTP_USERNAME']

            # Check if user is already playing
            if ServerConfig.get_sessionmanager().exists_with_username(username):
                return False

            # Apply user limit
            if ServerConfig.get_sessionmanager().user_count() >= ServerConfig.lobby_max_players:
                return False

            # Add user to local user cache
            user = LocalUser(sid, username)

            db_user = ServerConfig.get_database().get_user(user)
            user.db_id = db_user.id

            ServerConfig.get_sessionmanager().add_user(user)

            # Trigger event
            for user_ in ServerConfig.get_sessionmanager().users:
                if user_.id == sid:
                    continue
                chat_messages = []
                for _chat_message in ServerConfig.get_database().get_chat_messages_private(user.db_id, user_.db_id):
                    chat_messages.append(LocalChatMessage(
                        db_id=_chat_message.id,
                        from_user=_chat_message.from_user,
                        to_user=_chat_message.to_user,
                        message=_chat_message.message,
                        created=_chat_message.created
                    ))
                self.send(Event(EventType.USER_JOIN, {
                    'user': user,
                    'chat_messages': chat_messages
                }), to=user_.id)

            return True

        @self._sio.event
        def sync(sid):
            print('message ', sid)
            chat_messages = []
            for _chat_message in ServerConfig.get_database().get_chat_messages_global():
                chat_messages.append(LocalChatMessage(
                    db_id=_chat_message.id,
                    from_user=_chat_message.from_user,
                    to_user=_chat_message.to_user,
                    message=_chat_message.message,
                    created=_chat_message.created
                ))
            self.send(Event(EventType.SYNC, {
                'users': ServerConfig.get_sessionmanager().users,
                'chat_messages': chat_messages
            }), to=sid)

        @self._sio.event
        def lobby_ready(sid, data):
            # Check if Game is already running
            if ServerConfig.get_game() is not None:
                return

            # Check if Lobby has enough users
            users = ServerConfig.get_sessionmanager().users
            if len(users) < 2:
                return

            # Mark User as Ready
            user = ServerConfig.get_sessionmanager().get_user(sid)
            user.ready = data.ready
            ServerConfig.get_sessionmanager().update_user(user)

            # Check if every player is ready
            all_ready = True
            for user_ in users:
                if not user_.ready:
                    all_ready = False
            if all_ready:
                game = ServerConfig.create_game([user_.id for user_ in users])
                # Start Gameplay
                self.send(Event(EventType.GAMEPLAY_START))

                # Select user to move first
                next_player = game.next_player_to_move()
                self.send(Event(EventType.GAMEPLAY_MOVE_REQUEST), to=next_player)

        @self._sio.event
        def chat_message(sid, data):
            _chat_message = LocalChatMessage(
                from_user=ServerConfig.get_sessionmanager().get_user(sid).db_id,
                to_user=data['chat_message']['to_user'],
                message=data['chat_message']['message'],
                created=round(time.time()*1000)
            )
            ServerConfig.get_database().chat_message(_chat_message)

            self.send(Event(EventType.CHAT_MESSAGE, {
                'chat_messages': [
                    chat_message
                ]
            }))

        @self._sio.event
        def gameplay_move_response(sid, data):
            # Check if Game is running
            if ServerConfig.get_game() is None:
                return
            game = ServerConfig.get_game()

            # Make board move
            success = game.handle_turn(data.x, data.y)
            if not success:
                self.send(Event(EventType.GAMEPLAY_MOVE_DENIED), to=game.current_player)
                return

            # Send back that the move was accepted
            self.send(Event(EventType.GAMEPLAY_MOVE_ACCEPTED), to=game.current_player)

            if game.check_winner():
                self.send(Event(EventType.GAMEPLAY_STOP))
                self.send(Event(EventType.GAMEPLAY_WINNER, {
                    'user': game.current_player
                }))
                ServerConfig.get_database().game_over(game)
                return

            # Select user to move next
            next_player = game.next_player_to_move()
            self.send(Event(EventType.GAMEPLAY_MOVE_REQUEST), to=next_player)

        @self._sio.event
        def disconnect(sid):
            print('disconnect ', sid)
            # Check if user is in local user cache
            if not ServerConfig.get_sessionmanager().exists_with_id(sid):
                return False

            # Get user from local user cache
            user = ServerConfig.get_sessionmanager().get_user(sid)

            # Trigger event
            self.send(Event(EventType.USER_LEAVE, {'user': user}), skip_sid=sid)

            # Save and Remove user from local user cache
            ServerConfig.get_database().save_user(user)
            ServerConfig.get_sessionmanager().remove_user(sid)

            return True
