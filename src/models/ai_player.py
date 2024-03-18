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


class SmartAIPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 1 = X, 2 = O
        self.opponent_symbol = 2 if symbol == 1 else 1

    # returns the index of the possible best move
    def find_best_move(self, game):
        best_score = -100
        best_move = (-1, -1)  # row, col
        for row in range(3):
            for col in range(3):
                if game.board[row][col] == 0:  # do move if field is empty
                    game.board[row][col] = self.symbol
                    score = self.minimax(game, 0, False)
                    game.board[row][col] = 0  # Undo move
                    if (
                        score > best_score
                    ):  # if score is better than the current best score -> update best
                        best_score = score
                        best_move = (row, col)
        return best_move[0] * 3 + best_move[1]  # Convert row, col to index

    def minimax(self, game, depth, isMaximizing):
        print("Depth: ", depth, "is cheking for winner")
        winner = self.check_theoretical_winner(game)
        print("TheorieWinner: ", winner)
        if winner == self.symbol:
            return 1
        if winner == self.opponent_symbol:
            return -1
        elif all(
            game.board[row][col] != 0 for row in range(3) for col in range(3)
        ):  # Board is full
            return 0

        if isMaximizing:
            best_score = -100
            for row in range(3):
                for col in range(3):
                    if game.board[row][col] == 0:
                        game.board[row][col] = self.symbol
                        score = self.minimax(game, depth + 1, False)
                        game.board[row][col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 100
            for row in range(3):
                for col in range(3):
                    if game.board[row][col] == 0:
                        game.board[row][col] = self.opponent_symbol
                        score = self.minimax(game, depth + 1, True)
                        game.board[row][col] = 0
                        best_score = min(score, best_score)
            return best_score

    def make_move(self, game):
        index = self.find_best_move(game)
        print("Berechneter Index KI: ", index)
        return index

    def check_theoretical_winner(self, game):

        for i in range(3):
            # check for rows
            if game.board[i][0] == game.board[i][1] == game.board[i][2] != 0:
                return game.board[i][0]
            # check for colums
            if game.board[0][i] == game.board[1][i] == game.board[2][i] != 0:
                return game.board[0][i]
        # check for diagonals
        if (
            game.board[0][0] == game.board[1][1] == game.board[2][2] != 0
            or game.board[0][2] == game.board[1][1] == game.board[2][0] != 0
        ):
            return game.board[1][1]
        return 0

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
