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
        queenside_castle = create_move_from_str(board,'0-0-0',Color.WHITE)
        kingside_castle = create_move_from_str(board,'0-0',Color.WHITE)
        copyboard = board.create_successor_board(queenside_castle)
        self.assertTrue(copyboard.get_king_location(Color.WHITE) == (0,2))
        self.assertTrue(any([isinstance(piece,Rook) and piece.get_loc() == (0,3) for piece in copyboard.get_pieces(Color.WHITE)]))
        copyboard = board.create_successor_board(kingside_castle)
        self.assertTrue(copyboard.get_king_location(Color.WHITE) == (0, 6))
        self.assertTrue(
            any([isinstance(piece, Rook) and piece.get_loc() == (0, 5) for piece in copyboard.get_pieces(Color.WHITE)]))

unittest.main()