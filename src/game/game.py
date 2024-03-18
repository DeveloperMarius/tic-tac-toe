import random

from ..models.ai_player import DummyAIPlayer
from ..models.ai_player import SmartAIPlayer

from ..models.player import Player
from ..windows.components.tictactoe_field import FieldRect


class Game:

    def __init__(self, difficulty: int = 0) -> None:
        self.winner = 0
        # 0 = Nothing
        # 1 = X
        # 2 = O
        # randomly chosses the order of the players ([1, 2] or [2, 1])
        self.players = random.sample([1, 2], 2)
        self.player_1 = Player("Player 1", self.players[0])
        match difficulty:
            case 0:

                self.player_2 = DummyAIPlayer("Player 2", self.players[1])
            case 1:

                self.player_2 = SmartAIPlayer("Player 2", self.players[1])
            case _:
                self.player_2 = SmartAIPlayer("Player 2", self.players[1])

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
        print("Index: " + str(index) + " Symbol: " + str(self.current_player.symbol))
        print("Board: ", (index // 3), (index % 3))
        self.board[index // 3][index % 3] = self.current_player.symbol
        print(
            "Player "
            + str(self.current_player)
            + " checked field "
            + str(index)
            + " with symbol "
            + str(self.current_player.symbol)
        )

        # Check for winner
        if winner := self.check_winner():
            return winner

        # Change the current player
        self.switch_player()

        # let ai player make a move
        if (
            isinstance(self.current_player, (DummyAIPlayer, SmartAIPlayer))
            and self.winner == 0
        ):
            print("AI is making a move")
            index = self.current_player.make_move(self)
            fields = self.handle_turn(index, fields)

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

    def check_winner(self) -> int:

        if self.hoizontal_win():
            self.winner = self.current_player
            print("Player " + self.winner.name + " has won with horizontal position")
            return self.current_player.symbol

        if self.vertical_win():
            self.winner = self.current_player
            print("Player " + self.winner.name + " has won with vertical position")
            return self.current_player.symbol

        if self.diagonal_win():
            self.winner = self.current_player
            print("Player " + self.winner.name + " has won with diagonal position")
            return self.current_player.symbol

        # check if board is full
        if all(self.board[row][col] != 0 for row in range(3) for col in range(3)):
            print("The game ended in a draw")
            return 3

        return 0

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

    def handle_ai_first(self, fields: list[FieldRect]):
        if isinstance(self.current_player, (DummyAIPlayer, SmartAIPlayer)):
            index = self.current_player.make_move(self)
            print("AI is making a first move - is random")
            fields = self.handle_turn(index, fields)
        return fields

    def check_winner2(self) -> int:

        if self.hoizontal_win():
            return self.current_player.symbol

        if self.vertical_win():
            return self.current_player.symbol

        if self.diagonal_win():
            return self.current_player.symbol

        # check if board is full
        # if all(self.board[row][col] != 0 for row in range(3) for col in range(3)):
        # print("The game ended in a draw")
        # return 1

        return 0
