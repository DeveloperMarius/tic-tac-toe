from src.game.network import NetworkClient
import time
from src.game.config import ClientConfig
from src.game.events import EventType

s = NetworkClient('marius')
s._connect()
while True:
    print('users', ClientConfig.get_sessionmanager().users)
    time.sleep(20)

#with NetworkClient() as s:
#    print('runnning')
#    time.sleep(3)
#    s.sio.emit('my_message', {'message': 'my message'})
#    time.sleep(3)
