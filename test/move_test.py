from chess.chess_utils import convert_rank_file_to_int as convert
from chess.game_board import Board
from chess.chess_piece import *
import unittest
class MoveTest(unittest.TestCase):
    def test_move_from_str(self):
        board = Board().new_game()
        move_expr = 'Pa2a4'
        expected = Move(board,src=(1,0),dest=(3,0),color=Color.WHITE)

        actual = create_move_from_str(board,move_expr,Color.WHITE)
        self.assertEqual(expected,actual)
        try:
            move_expr = 'this should fail!'
            move = create_move_from_str(board,move_expr,Color.WHITE)
            self.fail('bad move did not throw exception')
        except:
            pass
    def test_get_all_moves(self):
        board = Board.load_from_file('test_data/sample_board1.txt')
        move_strs = ['kb1a1','kb1b2','kb1a2','kb1c1','kb1c2']
        expected = [create_move_from_str(board,move_str,Color.WHITE) for move_str in move_strs]
        actual = board.get_all_moves(Color.WHITE)
        for move in actual:
            self.assertIn(move,expected)




if __name__ == '__main__':
    unittest.main()
