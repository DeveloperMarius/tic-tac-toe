from src.game.game import Game
import symbol


class Player:

    def __init__(self, name, symbol):

        self.name = name
        self.symbol = symbol # 1 = X or 2 = O
        #self.game_stats = GameStats(name) # Game Stats noch nicht vorhanden

    def make_move(self, game, row: int, col: int):
        if game.player == self.symbol:  # check ob der Spieler an der Reihe ist
            index = row * 3 + col
            # aktuelles board abrufen
            if game.board[index // 3][index % 3] == 0:  # Feld ist frei
                game.handle_turn(index, game.board)
                return True
            else:
                return False
            # TODO: Check wenn das Spiel vorbei ist
            if game.check_winner():
                self.update_game_stats(winner=True)
                # TODO: Gewinnmeldung
            else:
                self.update_game_stats(winner=False)
    
    def update_game_stats(self, winner: bool):
        return 1

