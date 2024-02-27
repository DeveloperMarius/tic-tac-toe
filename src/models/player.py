from src.game.game import Game
import symbol


class Player:

    def __init__(self, name, symbol):

        self.name = name
        self.symbol = symbol # 1 = X or 2 = O
        self.game_stats = GameStats(name) # Game Stats noch nicht vorhanden

    def make_move(self, game, row: int, col: int):
        return 1
    
    def update_game_stats(self, winner: bool):
        return 1

