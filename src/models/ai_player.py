import random


class DummyAIPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 1 = X or 2 = O
        self.isMyTurn = False

    def make_random_move(self, game):
        # check for free boxes on board
        available_moves = [
            (row, col)
            for row in range(3)
            for col in range(3)
            if game.board[row][col] == 0
        ]
        print("Available moves: ", available_moves)
        # choose a random move between the available ones
        row, col = random.choice(available_moves)
        print("Random: ", row, col)
        index = row * 3 + col
        print("Index: ", index)
        return index

