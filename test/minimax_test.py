import unittest
from ai.minimax_agent import *
from ai.agent import *
from chess_lib.game_board import Board

class MinimaxTestCase(unittest.TestCase):
    def test_makes_optimal_move(self):
        board0 = Board.load_from_file('test_data/sample_board4.txt')
        board_minimax = board0.__deepcopy__()
        board_alphabeta= board0.__deepcopy__()
        black_minimax = pu(color=Color.BLACK)
        # black_alphabeta = PieceValueAlphaBeta(color=Color.BLACK)





if __name__ == '__main__':
    unittest.main()
