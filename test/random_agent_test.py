import unittest
from chess.game_board import Board
from chess.chess_utils import Color
from ai.agent import RandomAgent
class RandomAgentTest(unittest.TestCase):
    def test_random_agent_only_one_move(self):
        rand_agent = RandomAgent(color=Color.WHITE)
        board = Board.load_from_file('test_data/test_random_move.txt')
        pieces = board.get_pieces(Color.WHITE)
        pawn, loc = pieces[0]
        expected = pawn.get_valid_moves(board,loc)[0]
        print(expected)
        actual = rand_agent.get_next_move(board)
        print(actual)
        self.assertEqual(expected,actual)

unittest.main()