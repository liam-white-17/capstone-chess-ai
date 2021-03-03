from chess.chess_utils import convert_rank_file_to_int as convert, is_check, is_checkmate
from chess.game_board import Board
from chess.chess_piece import *
import unittest
class MiscTests(unittest.TestCase):
    def testConverterValues(self):
        rf = 'a1'
        expected = (0, 0)
        actual = convert(rf)
        self.assertEqual(expected,actual)
        rf = 'c7'
        expected = (6,2)
        actual = convert(rf)
        self.assertEqual(expected,actual)
        try:
            rf = 'z9'
            convert(rf)
            self.fail('Converter not throwing exception properly')
        except:
            pass
    def test_converter_on_board(self):
        board = Board().new_game()
        rf = 'b1'
        loc = convert(rf)
        piece = board.square_at(*loc).get_piece()
        self.assertIsInstance(piece,Knight)
        self.assertTrue(piece.get_color())
    def test_inv(self):
        white = Color.WHITE
        self.assertEqual(Color.BLACK,~white)
    def test_check(self):
        board = Board.load_from_file('test_data/sample_board_king_in_check.txt')
        self.assertTrue(is_check(board,Color.WHITE))
        board=Board().new_game()
        self.assertFalse(is_check(board,Color.WHITE))
    def test_checkmate(self):
        board = Board.load_from_file('test_data/test_checkmate.txt')
        self.assertTrue(is_checkmate(board,Color.WHITE))
        self.assertFalse(is_checkmate(board,Color.BLACK))

if __name__ == '__main__':
    unittest.main()