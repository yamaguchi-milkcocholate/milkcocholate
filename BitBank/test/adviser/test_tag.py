import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.adviser.tag import Tag


class TestTag(unittest.TestCase):

    def setUp(self):
        self.ema_term = 5
        self.ma_term = 9
        self.adviser = Tag(
            ema_term=5,
            ma_term=9,
            buy_directory='../../15min/training/aggregate_gp_07.pkl',
            sell_directory='../../15min/training/gp_next_10.pkl'
        )

    def tearDown(self):
        pass

    def test_find_maker(self):
        board = self.adviser.find_maker(side='bids')
        print(board)


if __name__ == '__main__':
    unittest.main()
