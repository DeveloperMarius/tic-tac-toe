import random

from src.game.network import NetworkClient
import time

usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
s = NetworkClient(random.choice(usernames))
s._connect()
while True:
    time.sleep(20)

#with NetworkClient() as s:
#    print('runnning')
#    time.sleep(3)
#    s.sio.emit('my_message', {'message': 'my message'})
#    time.sleep(3)
