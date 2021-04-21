import unittest
from chess_lib.game_board import Board
from ai.minimax_agent import *
from chess_lib.chess_piece import create_move_from_str
class MichniewskiTest(unittest.TestCase):
    def test_expected_utility(self):
        board = Board()
        board.new_game()
        white_agent = MichniewskiAgent(color=Color.WHITE)
        white_agent.max_depth = 2
        expected = 0
        actual = white_agent.evaluation_function(board,Color.WHITE)
        self.assertEqual(expected,actual)
        expected_moves = [create_move_from_str(board,'pe2e4',Color.WHITE),create_move_from_str(board,'pd2d4',Color.WHITE)]
        # actual_move = white_agent.get_next_move(board)
        # print(actual_move)
        # self.assertTrue(actual_move in expected_moves)
        # white_agent.max_depth = 4
        # expected_moves = [create_move_from_str(board, 'pe2e4', Color.WHITE),
        #                   create_move_from_str(board, 'pd2d4', Color.WHITE)]
        # actual_move = white_agent.get_next_move(board)
        # self.assertTrue(actual_move in expected_moves)

        copy_board = board.create_successor_board(expected_moves[0])
        expected = 40
        actual = white_agent.evaluation_function(copy_board,Color.WHITE)
        self.assertEqual(expected,actual)
    def test_optimal_move_skew(self):
        black_AI = MichniewskiAgent(color=Color.BLACK)
        white_ai = MichniewskiAgent(color=Color.WHITE)

        board = Board.load_from_file('optimality_test_boards/test_black_skew.txt')
        #print(piece_value_evaluation(board, Color.BLACK))
        board = board.create_successor_board(create_move_from_str(board, 'Qa3b4', Color.WHITE))
        #print(piece_value_evaluation(board, Color.BLACK))
        expected = create_move_from_str(board, 'ra7a1', Color.BLACK)
        actual = black_AI.get_next_move(board)
        self.assertEqual(expected, actual)
        board = board.create_successor_board(expected)
        expected = create_move_from_str(board, 'kc1c2', Color.WHITE)
        actual = white_ai.get_next_move(board)
        self.assertEqual(expected, actual)
        board = board.create_successor_board(expected)
        expected = create_move_from_str(board, 'ra1h1', Color.BLACK)
        actual = black_AI.get_next_move(board)
        self.assertEqual(expected, actual)
    def test_optimality_fork(self):
        board = Board.load_from_file('optimality_test_boards/milestone_demo_board1.txt')
        black_ai = MichniewskiAgent(color=Color.BLACK)
        white_move = create_move_from_str(board,'pa2a4',Color.WHITE)
        board = board.create_successor_board(white_move)
        expected = create_move_from_str(board,'hb4c2',Color.WHITE)
        actual = black_ai.get_next_move(board)
        self.assertEqual(expected,actual)

unittest.main()
