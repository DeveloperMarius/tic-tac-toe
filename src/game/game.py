import random

from ..models.player import Player
from ..windows.components.tictactoe_field import FieldRect


class Game:

    def __init__(self) -> None:
        self.winner = 0
        # 0 = Nothing
        # 1 = X
        # 2 = O
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
        # checks if a winner already exists
        if self.winner != 0:
            return False

        # Update the field
        fields[index].checked = self.current_player.symbol
        self.board[index // 3][index % 3] = self.current_player.symbol
        print(
            "Player "
            + str(self.current_player)
            + " checked field "
            + str(index)
            + " with symbol "
            + str(self.current_player.symbol)
        )
        # Change the current player
        switch_player(self)

        # Check for winner
        self.check_winner()

        return fields

    # checks whether one of the rows in the board contains three identical and non-zero values
    def hoizontal_win(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != 0:
                return True
        return False

    # checks whether one of the columns in the board contains three identical and non-zero values
    def vertical_win(self):
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return True
        return False

    # checks whether one of the diagonals in the board contains three identical and non-zero values
    def diagonal_win(self):
        # Diagonal from left to right
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return True
        # Diagonal from right to left
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return True
        return False

    def check_winner(self) -> bool:

        if self.hoizontal_win():
            self.winner = self.current_player
            print("Player " + self.winner.name + " has won with horizontal position")
            return True

        if self.vertical_win():
            self.winner = self.current_player
            print("Player " + self.winner.name + " has won with vertical position")
            return True

        if self.diagonal_win():
            self.winner = self.current_player
            print("Player " + self.winner.name + " has won with diagonal position")
            return True

        return False


# Switches the player and set the isMyTurn attribute
def switch_player(self):
    if self.current_player == self.player_1:
        self.current_player = self.player_2
        self.player_1.isMyTurn = False
        self.player_2.isMyTurn = True
    else:
        self.current_player = self.player_1
        self.player_2.isMyTurn = False
        self.player_1.isMyTurn = True
