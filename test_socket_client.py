import random

from src.game.network import NetworkClient
import time
from src.game.config import ClientConfig
from src.game.events import EventType

usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
s = NetworkClient(random.choice(usernames))
s._connect()
while True:
    def start():
        print('start')
    ClientConfig.get_eventmanager().on(EventType.GAMEPLAY_START, start)
    time.sleep(20)

#with NetworkClient() as s:
#    print('runnning')
#    time.sleep(3)
#    s.sio.emit('my_message', {'message': 'my message'})
#    time.sleep(3)
