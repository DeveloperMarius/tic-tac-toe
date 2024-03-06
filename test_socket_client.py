import random
from src.game.network import NetworkClient
from main import Main

usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
s = NetworkClient(random.choice(usernames))
s.connect()
Main()
