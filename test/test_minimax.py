import unittest
from ai.minimax_agent import *
from chess_lib.game_board import Board
from chess_lib.move import *


class MinimaxTest(unittest.TestCase):
    def test_black_can_skew(self):
        black_AI = PieceValueAgent(color=Color.BLACK,depth=3)
        white_ai = PieceValueAgent(color=Color.WHITE,depth=3)

        board = Board.load_from_file('optimality_test_boards/test_black_skew.txt')
        print(piece_value_evaluation(board, Color.BLACK))
        board = board.create_successor_board(create_move_from_str(board,'Qa3b4',Color.WHITE))
        print(piece_value_evaluation(board, Color.BLACK))
        expected = create_move_from_str(board,'ra7a1',Color.BLACK)
        actual = black_AI.get_next_move(board)
        self.assertEqual(expected,actual)
        board = board.create_successor_board(expected)
        expected = create_move_from_str(board,'kc1c2',Color.WHITE)
        actual = white_ai.get_next_move(board)
        self.assertEqual(expected,actual)
        board = board.create_successor_board(expected)
        expected = create_move_from_str(board,'ra1h1',Color.BLACK)
        actual = black_AI.get_next_move(board)
        self.assertEqual(expected,actual)



if __name__ == '__main__':
    unittest.main()
