from src.game.network import NetworkClient
import time
from src.game.config import Config
from src.game.events import EventType

s = NetworkClient('marius')
Config.get_eventmanager().on(EventType.USER_LEAVE, lambda event: print(event))
s._connect()
while True:
    time.sleep(20)

#with NetworkClient() as s:
#    print('runnning')
#    time.sleep(3)
#    s.sio.emit('my_message', {'message': 'my message'})
#    time.sleep(3)
