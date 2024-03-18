import random
import time

from src.game.config import ClientConfig
from src.game.events import EventType, Event
from src.game.network import NetworkClient

usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
s = NetworkClient.get_instance()
s.connect(random.choice(usernames), '127.0.0.1')
ClientConfig.get_eventmanager().on(EventType.CHAT_MESSAGE, lambda event: print(event))
for i in range(10):
    s.send(Event(EventType.CHAT_MESSAGE, {
        "chat_message": {
            'message': 'Hello World',
            'to_user': None
        }
    }))
    NetworkClient.get_instance().send(Event(EventType.CHAT_MESSAGE, {
        "chat_message": {
            'message': 'Hello World',
            'to_user': None
        }
    }))

while True:
    time.sleep(5)
# Main()