from src.game.game import Game
import unittest


class TestGameWinnerCondsitions(unittest.TestCase):

    def test_horizontal_win_first_row(self):
        game = Game()
        game.board = [
            [1, 1, 1],  # This represents a winning condition for X in the first row
            [0, 0, 0],
            [0, 0, 0],
        ]
        game.current_player = game.player_1  # Assuming player 1 is X
        self.assertTrue(game.hoizontal_win(), "Horizontal win (first row) not detected")


if __name__ == "__main__":
    unittest.main()
