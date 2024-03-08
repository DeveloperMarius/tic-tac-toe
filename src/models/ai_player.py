from player import Player


class AIPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.isMyTurn = False

    def make_move(self, game):
        if game.player == self.symbol:
            index = self.minimax(game, self.symbol)
            game.handle_turn(index, game.board)

            if game.check_winner():
                self.update_game_stats(winner=True)
            else:
                self.update_game_stats(winner=False)
