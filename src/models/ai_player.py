from concurrent.futures import ThreadPoolExecutor
import random

from ..windows.notification_manager import NotificationManager


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

    def make_move(self, game):
        return self.make_random_move(game)


class SmartAIPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 1 = X, 2 = O
        self.opponent_symbol = 2 if symbol == 1 else 1

    # calculate index for the best move
    def find_best_move(self, game):
        if all(game.board[row][col] == 0 for row in range(3) for col in range(3)):
            return random.choice([0, 2, 6, 8])  # Prioritize corners on an empty board
        best_score = -float("inf")
        best_move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if game.board[row][col] == 0:
                    game.board[row][col] = self.symbol
                    score = self.minimax(game, 0, False)
                    game.board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move[0] * 3 + best_move[1]

    # calculate the best score for a move with minimax algorithm
    def minimax(self, game, depth, isMaximizing):
        winner = self.check_theoretical_winner(game)
        if winner == self.symbol:
            return 10 - depth
        if winner == self.opponent_symbol:
            return depth - 10
        if all(game.board[row][col] != 0 for row in range(3) for col in range(3)):
            return 0

        if isMaximizing:
            best_score = -float("inf")
            for row in range(3):
                for col in range(3):
                    if game.board[row][col] == 0:
                        game.board[row][col] = self.symbol
                        score = self.minimax(game, depth + 1, False)
                        game.board[row][col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(3):
                for col in range(3):
                    if game.board[row][col] == 0:
                        game.board[row][col] = self.opponent_symbol
                        score = self.minimax(game, depth + 1, True)
                        game.board[row][col] = 0
                        best_score = min(score, best_score)
            return best_score

    # make a move
    def make_move(self, game):
        NotificationManager.get_instance().long_information("AI is thinking...")
        index = self.find_best_move(game)
        NotificationManager.get_instance().reset()
        print("Berechneter Index KI: ", index)
        return index

    # calculate the winner of the game
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
