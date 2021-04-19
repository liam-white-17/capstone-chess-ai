import unittest
from chess_lib.game_board import Board
from ai.minimax_agent import *
from chess_lib.chess_piece import create_move_from_str
class BasicLocationAgentTest(unittest.TestCase):
    def test_expected_utility(self):
        board = Board()
        board.new_game()
        white_agent = PieceLocationAgent(color=Color.WHITE)
        white_agent.max_depth = 2
        expected = 0
        actual = white_agent.evaluation_function(board,Color.WHITE)
        self.assertEqual(expected,actual)
        expected_moves = [create_move_from_str(board,'pe2e4',Color.WHITE),create_move_from_str(board,'pd2d4',Color.WHITE)]
        actual_move = white_agent.get_next_move(board)
        self.assertTrue(actual_move in expected_moves)
        white_agent.max_depth = 4
        expected_moves = [create_move_from_str(board, 'pe2e4', Color.WHITE),
                          create_move_from_str(board, 'pd2d4', Color.WHITE)]
        actual_move = white_agent.get_next_move(board)
        self.assertTrue(actual_move in expected_moves)
        copy_board = board.create_successor_board(actual_move)
        expected = 2.5
        actual = white_agent.evaluation_function(copy_board,Color.WHITE)
        self.assertEqual(expected,actual)
        black_move = create_move_from_str(board,'pd7d6',Color.BLACK)
        copy_board = board.create_successor_board(black_move)
        expected = 0.5
        actual = white_agent.evaluation_function(copy_board,Color.WHITE)

unittest.main()

