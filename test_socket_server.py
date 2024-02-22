import time

from src.game.network import NetworkServer

with NetworkServer() as s:
    print('running')
