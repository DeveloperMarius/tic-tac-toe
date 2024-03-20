import os
import time
import unittest
from typing import List

from socketio.exceptions import ConnectionError as SocketConnectionError

from src.game.config import Clients
from src.game.events import EventType, Event
from src.game.network import NetworkServer, NetworkClient


class TestUtils:

    awaited_event_data: List[Event] = []

    @staticmethod
    def await_event(event_type: EventType, timeout: int = 5) -> Event | None:
        start = time.time()
        while len([event for event in TestUtils.awaited_event_data if event.type == event_type]) == 0 and time.time() - start < timeout:
            TestUtils.awaited_event_data = []
            time.sleep(0.05)
        event = [event for event in TestUtils.awaited_event_data if event.type == event_type][0] if len([event for event in TestUtils.awaited_event_data if event.type == event_type]) > 0 else None
        TestUtils.awaited_event_data = []
        return event


class NetworkTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['env'] = "test"

        def await_event_callback(event: Event):
            TestUtils.awaited_event_data.append(event)
        Clients.first().get_eventmanager().on_any(lambda event: await_event_callback(event))
        Clients.second().get_eventmanager().on_any(lambda event: await_event_callback(event))

        server = NetworkServer.get_instance()
        server.start_server()

        Clients.first().set_username('Max')

    @classmethod
    def tearDownClass(cls):
        server = NetworkServer.get_instance()
        server.shutdown()

    def test_001_server_start(self):
        self.assertEqual(NetworkServer.get_instance().running, True)

    def test_002_client_connect_failed(self):
        self.assertRaises(SocketConnectionError, NetworkClient.first().connect, 'localhost', 7176)

    def test_003_client_connection(self):
        NetworkClient.first().connect('localhost', 7175)
        self.assertEqual(NetworkClient.first().connected, True)
        NetworkClient.first().disconnect()
        self.assertEqual(NetworkClient.first().connected, False)


class NetworkClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['env'] = "test"

        def await_event_callback(event: Event):
            TestUtils.awaited_event_data.append(event)
        Clients.first().get_eventmanager().on_any(lambda event: await_event_callback(event))
        Clients.second().get_eventmanager().on_any(lambda event: await_event_callback(event))

        server = NetworkServer.get_instance()
        server.start_server()

        Clients.first().set_username('Yin')

    @classmethod
    def tearDownClass(cls):
        server = NetworkServer.get_instance()
        server.shutdown()

    @classmethod
    def setUp(cls):
        NetworkClient.first().connect('localhost', port=7175)

    @classmethod
    def tearDown(cls):
        NetworkClient.first().disconnect()

    def test_000_third_player_connect(self):
        # Setup second user
        config2 = Clients.second()
        config2.set_username('Yang')
        NetworkClient.second().connect('localhost', 7175)

        # Setup third user
        config3 = Clients.add_client()
        config3.set_username('Yong')
        client3 = NetworkClient(2)

        self.assertRaises(SocketConnectionError, client3.connect, 'localhost', 7175)

        NetworkClient.second().disconnect()

    # Test sync event
    def test_001_client_connected(self):
        NetworkClient.first().send(Event(EventType.SYNC))
        event = TestUtils.await_event(EventType.SYNC)
        self.assertIsNotNone(event)
        self.assertEqual(EventType.SYNC, event.type)
        online_users = [user for user in event.data['users'] if user.online]
        self.assertEqual(1, len(online_users))
        self.assertEqual('Yin', online_users[0].username)

    # Test Chat
    def test_002_client_chat(self):
        NetworkClient.first().send(Event(EventType.CHAT_MESSAGE, {
            'chat_message': {
                'to_user': None,
                'from_user': Clients.first().get_user().id,
                'message': "Hello, World!"
            }
        }))
        event = TestUtils.await_event(EventType.CHAT_MESSAGE)
        self.assertIsNotNone(event)
        self.assertEqual(EventType.CHAT_MESSAGE, event.type)
        self.assertEqual(1, len(event.data['chat_messages']))
        self.assertEqual("Hello, World!", event.data['chat_messages'][0].message)
        self.assertEqual(Clients.first().get_user().id, event.data['chat_messages'][0].from_user)

    # Test Lobby Join and Leave
    def test_003_client_lobby(self):
        # Setup second user
        config2 = Clients.second()
        config2.set_username('Yang')
        NetworkClient.second().connect('localhost', 7175)

        # Test Join
        event = TestUtils.await_event(EventType.USER_JOIN)
        self.assertIsNotNone(event)
        self.assertEqual(EventType.USER_JOIN, event.type)
        self.assertEqual('Yang', event.data['user'].username)

        # Test Leave
        NetworkClient.second().disconnect()
        event = TestUtils.await_event(EventType.USER_LEAVE)
        self.assertIsNotNone(event)
        self.assertEqual(EventType.USER_LEAVE, event.type)
        self.assertEqual('Yang', event.data['user'].username)

    # Test Lobby Join and Ready
    def test_004_client_lobby_ready(self):
        # Setup second user
        config2 = Clients.second()
        config2.set_username('Yang')
        NetworkClient.second().connect('localhost', 7175)

        # Test Lobby Ready
        NetworkClient.second().send(Event(EventType.LOBBY_READY, {"ready": True}))
        event = TestUtils.await_event(EventType.USER_UPDATE)

        self.assertIsNotNone(event)
        self.assertEqual(EventType.USER_UPDATE, event.type)
        self.assertEqual(True, event.data['user'].ready)

        # Test Gameplay start
        NetworkClient.first().send(Event(EventType.LOBBY_READY, {"ready": True}))
        event = TestUtils.await_event(EventType.GAMEPLAY_START)

        self.assertIsNotNone(event)
        self.assertEqual(EventType.GAMEPLAY_START, event.type)

        NetworkClient.second().disconnect()

    # Test complete Gameplay over real network for win
    def test_005_client_gameplay_win(self):
        # Setup second user
        config2 = Clients.second()
        config2.set_username('Yang')
        NetworkClient.second().connect('localhost', 7175)
        # Send ready info
        NetworkClient.first().send(Event(EventType.LOBBY_READY, {"ready": True}))
        NetworkClient.second().send(Event(EventType.LOBBY_READY, {"ready": True}))
        # Wait for gameplay start and get first user to move
        first_user_event = TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        first_user = 0 if NetworkClient.first().config.get_user().username == first_user_event.reciever else 1

        # Send moves
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 0,
            'y': 0,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 1,
            'y': 0,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 1,
            'y': 1,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 2,
            'y': 0,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 2,
            'y': 2,
        }))

        # Wait for game end and check if the winner is correct
        event = TestUtils.await_event(EventType.GAMEPLAY_STOP)

        self.assertIsNotNone(event)
        self.assertEqual(EventType.GAMEPLAY_STOP, event.type)
        self.assertEqual(1, len(event.data['winners']))
        self.assertEqual(first_user_event.reciever, Clients.first().get_sessionmanager().get_user(event.data['winners'][0]).username)

    # Test complete Gameplay over real network for draw
    def test_006_client_gameplay_draw(self):
        # Setup second user
        config2 = Clients.second()
        config2.set_username('Yang')
        NetworkClient.second().connect('localhost', 7175)
        # Send ready info
        NetworkClient.first().send(Event(EventType.LOBBY_READY, {"ready": True}))
        NetworkClient.second().send(Event(EventType.LOBBY_READY, {"ready": True}))
        # Wait for gameplay start and get first user to move
        first_user_event = TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        first_user = 0 if NetworkClient.first().config.get_user().username == first_user_event.reciever else 1

        # Send moves
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 0,
            'y': 0,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 1,
            'y': 0,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 2,
            'y': 0,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 1,
            'y': 1,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 1,
            'y': 2,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 2,
            'y': 1,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 2,
            'y': 2,
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 0,
            'y': 2
        }))
        TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        (NetworkClient.first() if first_user == 0 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 0,
            'y': 1,
        }))

        # Wait for game end and check if the winner is correct
        event = TestUtils.await_event(EventType.GAMEPLAY_STOP)

        self.assertIsNotNone(event)
        self.assertEqual(EventType.GAMEPLAY_STOP, event.type)
        self.assertEqual(2, len(event.data['winners']))

    # Test Gameplay move denied and user leave in ongoing game
    def test_007_client_gameplay_leave(self):
        # Setup second user
        config2 = Clients.second()
        config2.set_username('Yang')
        NetworkClient.second().connect('localhost', 7175)
        # Send ready info
        NetworkClient.first().send(Event(EventType.LOBBY_READY, {"ready": True}))
        NetworkClient.second().send(Event(EventType.LOBBY_READY, {"ready": True}))
        # Wait for gameplay start and get first user to move
        first_user_event = TestUtils.await_event(EventType.GAMEPLAY_MOVE_REQUEST)
        first_user = 0 if NetworkClient.first().config.get_user().username == first_user_event.reciever else 1

        # Send moves
        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).send(Event(EventType.GAMEPLAY_MOVE_RESPONSE, {
            'x': 0,
            'y': 0,
        }))
        event = TestUtils.await_event(EventType.GAMEPLAY_MOVE_DENIED)
        self.assertIsNotNone(event)
        self.assertEqual(EventType.GAMEPLAY_MOVE_DENIED, event.type)

        (NetworkClient.first() if first_user == 1 else NetworkClient.second()).disconnect()

        # Wait for game end and check if the winner is correct
        event = TestUtils.await_event(EventType.GAMEPLAY_STOP)

        self.assertIsNotNone(event)
        self.assertEqual(EventType.GAMEPLAY_STOP, event.type)
        self.assertEqual(1, len(event.data['winners']))
        self.assertEqual(first_user_event.reciever, Clients.first().get_sessionmanager().get_user(event.data['winners'][0]).username)


if __name__ == '__main__':
    unittest.main()
