class TicTacToe:

    def __init__(self) -> None:
        # 0 = Nothing
        # 1 = X
        # 2 = O
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

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
