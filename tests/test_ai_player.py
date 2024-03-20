from unittest.mock import MagicMock
from src.models.ai_player import DummyAIPlayer, SmartAIPlayer
import unittest


class TestAIPlayers(unittest.TestCase):

    def setUp(self):
        # Mock-up for Game Class
        self.mock_game = MagicMock()
        self.mock_game.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def test_dummy_ai_random_move(self):
        dummy_ai = DummyAIPlayer("Dummy AI", 1)  # Symbol 1 -> X
        index = dummy_ai.make_move(self.mock_game)
        row, col = index // 3, index % 3
        self.assertEqual(
            self.mock_game.board[row][col],
            0,
            "Dummy AI should choose a free box",
        )

    def test_smart_ai_best_move(self):
        smart_ai = SmartAIPlayer("Smart AI", 1)  # Smart Ai has X
        # Set the board to a state in which Smart AI can win
        self.mock_game.board = [[1, 2, 0], [0, 1, 0], [2, 0, 0]]
        index = smart_ai.make_move(self.mock_game)
        expected_index = 8  # best position to win
        self.assertEqual(
            index, expected_index, "Smart AI should choose the best move to win"
        )

    def test_smart_ai_defensive_move(self):
        smart_ai = SmartAIPlayer("Smart AI", 2)  # Smart AI has O
        # Set the board to a state in which Smart AI must block the opponent
        self.mock_game.board = [[1, 2, 0], [0, 1, 0], [0, 0, 0]]
        index = smart_ai.make_move(self.mock_game)
        expected_index = 8  # best position to block
        self.assertEqual(
            index,
            expected_index,
            "Smart AI should choose the best move to block the opponent",
        )


if __name__ == "__main__":
    unittest.main()

# run tetst with: python3 -m tests.test_ai_player
