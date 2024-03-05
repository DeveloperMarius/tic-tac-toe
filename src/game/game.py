import random

from models.player import Player
from ..windows.components.tictactoe_field import FieldRect


class Game:

    def __init__(self) -> None:
        # 0 = Nothing
        # 1 = X
        # 2 = O
        self.winner = 0
        # randomly chosses the order of the players ([1, 2] or [2, 1])
        self.players = random.sample([1, 2], 2)
        self.player_1 = Player("Player 1", self.players[0])
        self.player_2 = Player("Player 2", self.players[1])
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        # set the player who starts
        if self.player_1.symbol == 1:
            self.player_1.isMyTurn = True
            self.current_player = self.player_1
        else:
            self.player_2.isMyTurn = True
            self.current_player = self.player_2

    def handle_turn(self, index: int, fields: list[FieldRect]):
        # Check if the field is already checked
        if self.board[index // 3][index % 3] != 0:
            return

        # Update the field
        fields[index].checked = self.player
        self.board[index // 3][index % 3] = self.player

        # Change the player
        self.player = 1 if self.player == 2 else 2

        # Check for winner
        self.check_winner()

        return fields

    def hoizontal_win(self):
        for row in self.board:
            symbol = row[0]
            if row == [symbol, symbol, symbol]:
                return True

        return False

    def vertical_win(self):
        list(zip(self.board[::-1]))

    def diagonal_win(self):
        pass

    def check_winner(self) -> bool:
        if self.hoizontal_win():
            return True

        if self.vertical_win():
            return True

        if self.diagonal_win():
            return True

        return False

# Switches the player and set the isMyTurn attribute
def switch_player(self):
    if self.current_player == self.player1:
        self.current_player = self.player2
        self.player1.isMyTurn = False
        self.player2.isMyTurn = True
    else:
        self.current_player = self.player1
        self.player2.isMyTurn = False
        self.player1.isMyTurn = True