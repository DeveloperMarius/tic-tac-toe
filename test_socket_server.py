import time

from main import Main
from src.game.network import NetworkServer, NetworkClient
import random

with NetworkServer.get_instance() as s:
    usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
    c = NetworkClient()
    c.connect(random.choice(usernames), '127.0.0.1')
    while True:
        time.sleep(5)
    # Main()
