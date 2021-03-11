from chess.chess_utils import convert_rank_file_to_int as convert
from chess.move import *
from chess.game_board import Board
from chess.chess_piece import *
import unittest
class CastleTest(unittest.TestCase):
    def test_can_kingside_castle_white(self):
        board = Board.load_from_file('test_data/test_kingside_castle_white.txt')
        pieces = board.get_pieces(Color.WHITE)
        moves = pieces[0][0].get_valid_moves(board,pieces[0][1])+pieces[1][0].get_valid_moves(board,pieces[1][1])
        self.assertTrue(any([isinstance(move,Castle) for move in moves]))
unittest.main()