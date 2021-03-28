import unittest
from chess_lib.chess_utils import convert_rank_file_to_int as convert
from chess_lib.game_board import Board
from chess_lib.chess_piece import *
import unittest


class TestPawnPromotion(unittest.TestCase):
    def test_pawn_promotion(self):
        board = Board.load_from_file('test_data/test_pawn_promotion.txt')
        white_pieces = board.get_pieces(Color.WHITE)
        black_pieces = board.get_pieces(Color.BLACK)
        for piece in white_pieces+black_pieces:
            if isinstance(piece,Pawn):
                moves = piece.get_valid_moves(board)
                for move in moves:
                    self.assertTrue(isinstance(move,PawnPromotion))


if __name__ == '__main__':
    unittest.main()
