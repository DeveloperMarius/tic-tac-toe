from src.game.game import Game
import unittest


class TestGameWinnerCondsitions(unittest.TestCase):

    def setUp(self):
        # Setup a game instance before each test
        self.game = Game()
        self.game.player_1.symbol = 1  # X
        self.game.player_2.symbol = 2  # O

    def test_horizontal_win_player_1(self):
        # Set the board for a horizontal win for player 1
        self.game.board = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
        self.game.current_player = self.game.player_1
        self.assertTrue(
            self.game.hoizontal_win(), "Horizontal win not detected for Player 1"
        )

    def test_vertical_win_player_2(self):
        # Set the board for a vertical win for player 2
        self.game.board = [[2, 0, 0], [2, 0, 0], [2, 0, 0]]
        self.game.current_player = self.game.player_2
        self.assertTrue(
            self.game.vertical_win(), "Vertical win not detected for Player 2"
        )


if __name__ == "__main__":
    unittest.main()

# run tetst with: python -m tests.test_win_conditions
