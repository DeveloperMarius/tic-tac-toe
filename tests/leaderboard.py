import random
import unittest


class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.leaderboard = [
            {"username": "test3", "wins": 3, "loses": 2, "draws": 6},
            {"username": "test2", "wins": 3, "loses": 2, "draws": 5},
            {"username": "test", "wins": 2, "loses": 3, "draws": 5},
        ]

    def test_sorting(self):
        leaderboard = random.shuffle(self.leaderboard)
        leaderboard.sort(key=lambda x: (-x["wins"], x["loses"], -x["draws"]))
        self.assertEqual(leaderboard, self.leaderboard)


if __name__ == "__main__":
    unittest.main()
