from chess.chess_utils import convert_rank_file_to_int as convert
from chess.game_board import Board
from chess.chess_piece import *
import unittest
class MoveTest(unittest.TestCase):
    def test_move_from_str(self):
        board = Board().new_game()
        move_expr = 'Pa2a4'
        expected = Move(board,src=(1,0),dest=(3,0),color=Color.WHITE)

        actual = Move.create_move_from_str(board,move_expr,Color.WHITE)
        self.assertEqual(expected,actual)
        try:
            move_expr = 'this should fail!'
            move = Move.create_move_from_str(board,move_expr,Color.WHITE)
            self.fail('bad move did not throw exception')
        except:
            pass


if __name__ == '__main__':
    unittest.main()
