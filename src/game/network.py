import imp
import socketio
from src.models.chat_message import LocalChatMessage, ChatMessage
from src.models.user import LocalUser
from src.game.config import ClientConfig, ServerConfig
from src.game.events import Event, EventType
import json
from src.utils.json_encoder import ModelEncoder
from threading import Thread
from aiohttp import web
import time
import asyncio

from src.windows.window_manager import WindowManager


class NetworkClient:

    _static_network_client = None

    @staticmethod
    def get_instance():
        if NetworkClient._static_network_client is None:
            NetworkClient._static_network_client = NetworkClient()
        return NetworkClient._static_network_client

    _sio: socketio.Client
    _username: str

    def __init__(self):
        self._sio = socketio.Client()

    def __enter__(self, username, host):
        self.connect(username, host)
        return self

    @property
    def username(self):
        return self._username

    def connect(self, username, host, port=7175):
        self._username = username
        self.call_backs()
        self._register_default_events()
        self._sio.connect(
            f"http://{host}:{port}", {"username": self.username}, "authtoken"
        )
        self.send(Event(EventType.SYNC))

    def disconnect(self):
        self._sio.disconnect()

    def _register_default_events(self):
        ClientConfig.get_eventmanager().clear_events()
        ClientConfig.get_eventmanager().on(
            EventType.USER_JOIN,
            lambda event: ClientConfig.get_sessionmanager().add_user(
                event.data["user"]
            ),
        )
        ClientConfig.get_eventmanager().on(
            EventType.USER_LEAVE,
            lambda event: ClientConfig.get_sessionmanager().remove_user(
                event.data["user"].id
            ),
        )
        ClientConfig.get_eventmanager().on(
            EventType.USER_UPDATE,
            lambda event: ClientConfig.get_sessionmanager().update_user(
                event.data["user"]
            ),
        )
        ClientConfig.get_eventmanager().on(
            EventType.CHAT_MESSAGE,
            lambda event: ClientConfig.get_sessionmanager().add_chat_messages(
                event.data["chat_messages"]
            ),
        )
        ClientConfig.get_eventmanager().on(
            EventType.SYNC, lambda event: self._event_sync(event)
        )
        ClientConfig.get_eventmanager().on(
            EventType.GAMEPLAY_START, lambda event: self._gameplay_start(event)
        )
        ClientConfig.get_eventmanager().on(
            # TODO Implement success message
            EventType.GAMEPLAY_MOVE_ACCEPTED, lambda event: print('Move accepted')
        )
        ClientConfig.get_eventmanager().on(
            # TODO Implement error message
            EventType.GAMEPLAY_MOVE_DENIED, lambda event: print('Move denied')
        )
        ClientConfig.get_eventmanager().on(
            # TODO Implement finish message / back to menu
            EventType.GAMEPLAY_STOP, lambda event: print('Move denied')
        )
        ClientConfig.get_eventmanager().on(
            EventType.GAMEPLAY_MOVE_ACCEPTED, lambda event: self._gameplay_move_accepted(event)
        )

    def _event_sync(self, event):
        ClientConfig.get_sessionmanager().set_users(event.data["users"])
        ClientConfig.get_sessionmanager().set_chat_messages(event.data["chat_messages"])

    def _gameplay_start(self, event):
        from ..windows.multiplayer_game_window import MultiplayerGameWindow

        WindowManager.get_instance().activeWindow = MultiplayerGameWindow()

    def _gameplay_move_accepted(self, event):
        fields = WindowManager.get_instance().activeWindow.tictactoe_field.field_rects
        fields[event.data['x'] + (event.data['y'] * 3)].checked = ClientConfig.get_sessionmanager().get_user(event.data['user_id']).game_symbol
        WindowManager.get_instance().activeWindow.tictactoe_field.field_rects = fields

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sio.disconnect()

    def call_backs(self):
        @self._sio.event
        def connect():
            print("connection established")

        @self._sio.on("*")
        def any_event(event, data):
            print("message received with ", event, data)
            parsed_data = json.loads(data)
            if "user" in parsed_data:
                parsed_data["user"] = LocalUser(**parsed_data["user"])
            if "chat_messages" in parsed_data:
                chat_messages = []
                for chat_message in parsed_data["chat_messages"]:
                    from_user = ClientConfig.get_sessionmanager().get_user_by_dbid(
                        chat_message["from_user"]
                    )
                    chat_messages.append(
                        LocalChatMessage(
                            from_user.id if from_user is not None else None,
                            chat_message["message"],
                            chat_message["created"],
                            (
                                ClientConfig.get_sessionmanager()
                                .get_user_by_dbid(chat_message["to_user"])
                                .id
                                if chat_message["to_user"] is not None
                                else None
                            ),
                            chat_message["db_id"],
                            chat_message["from_user_username"],
                        )
                    )
                parsed_data["chat_messages"] = chat_messages
            if "users" in parsed_data:
                users = []
                for user in parsed_data["users"]:
                    users.append(LocalUser(**user))
                parsed_data["users"] = users
            event_type = EventType(event)
            ClientConfig.get_eventmanager().trigger(Event(event_type, parsed_data))

        @self._sio.event
        def disconnect():
            print("disconnected from server")

    def send(self, event: Event):
        self._sio.emit(event.type.value, event.data)

    def send_request(self, event_type: EventType):
        self._sio.emit(event_type.value, {})


class NetworkServer:

    _static_network_server = None

    @staticmethod
    def get_instance():
        if NetworkServer._static_network_server is None:
            NetworkServer._static_network_server = NetworkServer()
        return NetworkServer._static_network_server

    _sio: socketio.AsyncServer
    running: bool = False

    def __init__(self):
        self._sio = socketio.AsyncServer()
        self.call_backs()
        self._app = web.Application()
        self._sio.attach(self._app)
        self._runner = web.AppRunner(self._app)
        self._thread = Thread(target=self._start_server)

    def __enter__(self):
        self.start_server()
        return self._sio

    def start_server(self):
        self._thread.start()
        time.sleep(5)

    def _start_server(self):
        asyncio.run(self._start_server2())

    async def _start_server2(self):
        print("Starting server")
        self.running = True
        await self._runner.setup()
        site = web.TCPSite(self._runner, "localhost", 7175)
        await site.start()
        while self.running:
            await asyncio.sleep(0.1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self.running = False
        time.sleep(3)
        asyncio.run(self._runner.cleanup())
        NetworkServer._static_network_server = None
        ServerConfig.reset()

    async def send(self, event: Event, to=None, skip_sid=None):
        await self._sio.emit(
            event.type.value,
            json.dumps(event.data, cls=ModelEncoder),
            to=to,
            skip_sid=skip_sid,
        )

    def call_backs(self):
        @self._sio.event
        async def connect(sid, headers, auth):
            print("connect ", sid, headers, auth)
            username = headers["HTTP_USERNAME"]

            # Check if user is already playing
            if ServerConfig.get_sessionmanager().exists_with_username(username):
                return False

            # Apply user limit
            if (
                ServerConfig.get_sessionmanager().user_count()
                >= ServerConfig.lobby_max_players
            ):
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
                for (
                    _chat_message
                ) in ServerConfig.get_database().get_chat_messages_private(
                    user.db_id, user_.db_id
                ):
                    chat_messages.append(
                        LocalChatMessage(
                            db_id=_chat_message.id,
                            from_user=_chat_message.from_user,
                            to_user=_chat_message.to_user,
                            message=_chat_message.message,
                            created=_chat_message.created,
                            from_user_username=ServerConfig.get_database()
                            .get_user_by_id(_chat_message.from_user)
                            .username,
                        )
                    )
                await self.send(
                    Event(
                        EventType.USER_JOIN,
                        {"user": user, "chat_messages": chat_messages},
                    ),
                    to=user_.id,
                )

            return True

        @self._sio.event
        async def sync(sid, data):
            print("message ", sid)
            chat_messages = []
            for _chat_message in ServerConfig.get_database().get_chat_messages_global():
                chat_messages.append(
                    LocalChatMessage(
                        db_id=_chat_message.id,
                        from_user=_chat_message.from_user,
                        to_user=_chat_message.to_user,
                        message=_chat_message.message,
                        created=_chat_message.created,
                        from_user_username=ServerConfig.get_database()
                        .get_user_by_id(_chat_message.from_user)
                        .username,
                    )
                )
            await self.send(
                Event(
                    EventType.SYNC,
                    {
                        "users": ServerConfig.get_sessionmanager().users,
                        "chat_messages": chat_messages,
                    },
                ),
                to=sid,
            )

        @self._sio.event
        async def lobby_ready(sid, data):
            # Check if Game is already running
            if ServerConfig.get_game() is not None:
                return

            # Check if Lobby has enough users
            if len(ServerConfig.get_sessionmanager().users) < 2:
                return

            # Mark User as Ready
            user = ServerConfig.get_sessionmanager().get_user(sid)
            user.ready = data["ready"]
            ServerConfig.get_sessionmanager().update_user(user)
            await self.send(Event(EventType.USER_UPDATE, {"user": user}))

            # Check if every player is ready
            users = ServerConfig.get_sessionmanager().users
            all_ready = True
            for user_ in users:
                if not user_.ready:
                    all_ready = False
            if all_ready:
                game = ServerConfig.create_game([user_.id for user_ in users])

                # Assign user symbols
                for i in range(len(users)):
                    user_ = users[i]
                    user_.game_symbol = i+1
                    ServerConfig.get_sessionmanager().update_user(user_)
                    await self.send(Event(EventType.USER_UPDATE, {"user": user_}))

                # Start Gameplay
                ServerConfig.get_database().game_start(
                    game, ServerConfig.get_sessionmanager().users
                )
                await self.send(Event(EventType.GAMEPLAY_START, {}))

                # Select user to move first
                next_player = game.next_player_to_move()
                await self.send(
                    Event(EventType.GAMEPLAY_MOVE_REQUEST, {}), to=next_player
                )

        @self._sio.event
        async def user_update_username(sid, data):
            user = ServerConfig.get_sessionmanager().get_user(sid)
            user.username = data['username']
            ServerConfig.get_sessionmanager().update_user(user)
            ServerConfig.get_database().update_username(user)
            await self.send(Event(EventType.USER_UPDATE, {"user": user}))

        @self._sio.event
        async def chat_message(sid, data):
            _chat_message = LocalChatMessage(
                from_user=sid,
                to_user=data["chat_message"]["to_user"],
                message=data["chat_message"]["message"],
                created=round(time.time() * 1000),
                db_id=None,
                from_user_username=ServerConfig.get_sessionmanager()
                .get_user(sid)
                .username,
            )
            ServerConfig.get_database().chat_message(
                ChatMessage(
                    id=_chat_message.db_id,
                    from_user=ServerConfig.get_sessionmanager()
                    .get_user(_chat_message.from_user)
                    .db_id,
                    to_user=(
                        ServerConfig.get_sessionmanager()
                        .get_user(_chat_message.to_user)
                        .db_id
                        if _chat_message.to_user is not None
                        else None
                    ),
                    message=_chat_message.message,
                    created=_chat_message.created,
                )
            )
            if data["chat_message"]["to_user"] is None:
                await self.send(
                    Event(EventType.CHAT_MESSAGE, {"chat_messages": [_chat_message]})
                )
            else:
                await self.send(
                    Event(EventType.CHAT_MESSAGE, {"chat_messages": [_chat_message]}),
                    to=data["chat_message"]["to_user"],
                )

        @self._sio.event
        async def gameplay_move_response(sid, data):
            # Check if Game is running
            if ServerConfig.get_game() is None:
                return
            game = ServerConfig.get_game()

            # Check if user is allowed to move
            if sid != game.current_player:
                await self.send(
                    Event(EventType.GAMEPLAY_MOVE_DENIED, {
                        'message': 'Du bist nicht an der Reihe'
                    }), to=sid
                )
                return

            # Make board move
            success = game.handle_turn(data['x'], data['y'])
            if not success:
                await self.send(
                    Event(EventType.GAMEPLAY_MOVE_DENIED, {
                        'message': 'Du kannst in dieses Feld nicht setzen'
                    }), to=sid
                )
                return

            # Send back that the move was accepted
            await self.send(
                Event(EventType.GAMEPLAY_MOVE_ACCEPTED, {
                    'x': data['x'],
                    'y': data['y'],
                    'user_id': game.current_player
                })
            )

            if game.is_draw():
                await self.send(Event(EventType.GAMEPLAY_STOP, {
                    'result': 0
                }))
                for player in game.players:
                    ServerConfig.get_database().game_over(
                        game,
                        ServerConfig.get_sessionmanager().get_user(player),
                        0
                    )
                await self.send(
                    Event(EventType.GAMEPLAY_WINNER, {"winners": game.players})
                )
                return
            if game.check_winner():
                for player in game.players:
                    if player == game.current_player:
                        continue
                    ServerConfig.get_database().game_over(
                        game,
                        ServerConfig.get_sessionmanager().get_user(player),
                        1
                    )
                ServerConfig.get_database().game_over(
                    game,
                    ServerConfig.get_sessionmanager().get_user(game.current_player),
                    2
                )
                await self.send(
                    Event(EventType.GAMEPLAY_WINNER, {"winners": [
                        game.current_player
                    ]})
                )
                return

            # Select user to move next
            next_player = game.next_player_to_move()
            await self.send(Event(EventType.GAMEPLAY_MOVE_REQUEST), to=next_player)

        @self._sio.event
        async def disconnect(sid):
            print("disconnect ", sid)
            # Check if user is in local user cache
            if not ServerConfig.get_sessionmanager().exists_with_id(sid):
                return False

            # Get user from local user cache
            user = ServerConfig.get_sessionmanager().get_user(sid)

            # Trigger event
            await self.send(Event(EventType.USER_LEAVE, {"user": user}), skip_sid=sid)

            # Save and Remove user from local user cache
            ServerConfig.get_sessionmanager().remove_user(sid)

            return True
