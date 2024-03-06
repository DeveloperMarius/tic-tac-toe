from main import Main
from src.game.network import NetworkServer, NetworkClient
import random

with NetworkServer() as s:
    usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
    c = NetworkClient(random.choice(usernames))
    c.connect()
    Main()
