from chess_lib.chess_utils import convert_rank_file_to_int as convert
from chess_lib.move import *
from chess_lib.game_board import Board
from chess_lib.chess_piece import *
import unittest
class CastleTest(unittest.TestCase):
    def test_can_kingside_castle_white(self):
        board = Board.load_from_file('test_data/test_kingside_castle_white.txt')
        moves = board.get_all_moves(Color.WHITE)
        self.assertTrue(any([isinstance(move,Castle) and not move.is_queenside for move in moves]))
unittest.main()