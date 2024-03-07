class Player:

    def __init__(self, name, symbol):

        self.name = name
        self.symbol = symbol  # 1 = X or 2 = O
        self.isMyTurn = False
        # self.game_stats = GameStats(name) # Game Stats noch nicht vorhanden

    def make_move(self, game, row: int, col: int):
        if game.player == self.symbol:  # check ob der Spieler an der Reihe ist
            index = row * 3 + col
            # handle auslösen
            game.handle_turn(index, game.board)

            # TODO: Check wenn das Spiel vorbei ist
            if game.check_winner():
                self.update_game_stats(winner=True)
                # TODO: Gewinnmeldung
            else:
                self.update_game_stats(winner=False)

    def update_game_stats(self, winner: bool):
        return 1
