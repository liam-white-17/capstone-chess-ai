import unittest
from chess_lib.game_board import Board
from chess_lib.chess_utils import Color
from ai.agent import RandomAgent
class RandomAgentTest(unittest.TestCase):
    def test_random_agent_only_one_move(self):
        rand_agent = RandomAgent(color=Color.WHITE)
        board = Board.load_from_file('test_data/test_random_move.txt')
        pieces = board.get_pieces(Color.WHITE)
        pawn = pieces[0]
        expected = pawn.get_valid_moves(board)[0]
        actual = rand_agent.get_next_move(board,no_moves_to_check=False)
        self.assertEqual(expected,actual)

unittest.main()