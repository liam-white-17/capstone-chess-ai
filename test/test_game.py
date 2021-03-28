import unittest
from unittest.mock import patch
from game.game import ChessGame
from chess_lib.chess_utils import Color
from chess_lib.chess_piece import *
class BoardTest(unittest.TestCase):
    @patch('builtins.input',side_effect=['kd3d4','kd3e3'])
    def test_cant_move_to_check(self,mock_input):
        mygame = ChessGame(load_file='test_data/test_king_cannot_move_to_check.txt')
        pre = mygame.board
        white_pieces = mygame.board.get_pieces(Color.WHITE)
        self.assertTrue((King(is_white=Color.WHITE),(2,3)) in white_pieces)
        #black_pieces = mygame.board.get_pieces(Color.BLACK)
        move=mygame.get_next_move()
        mygame.process_move(move)

        post = mygame.board
        self.assertEqual(pre,post)
        white_pieces=mygame.board.get_pieces(Color.WHITE)
        self.assertFalse((King(is_white=Color.WHITE),(3,3)) in white_pieces)
        self.assertTrue((King(is_white=Color.WHITE),(2,3)) in white_pieces)
        move=mygame.get_next_move()
        mygame.process_move(move)
        post = mygame.board
        print(post.display_board())
        white_pieces = post.get_pieces(Color.WHITE)
        print(white_pieces)
        self.assertTrue((King(is_white=Color.WHITE),(2,4)) in white_pieces)

unittest.main()
