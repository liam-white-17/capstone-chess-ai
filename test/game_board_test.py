import unittest
from chess_lib.game_board import *
class GameBoardTest(unittest.TestCase):
    def test_empty_board(self):
        board = Board()
        pieces = board.get_pieces(Color.WHITE)
        self.assertEqual(len(pieces), 0)
        pieces = board.get_pieces(Color.BLACK)
        self.assertEqual(len(pieces),0)

    def test_new_board(self):
        board=Board()
        board.new_game()

        self.assertEqual(len(board.get_pieces(Color.WHITE)),16)

        infile = open('test_data/new_board.txt','r')
        expected = infile.read()
        infile.close()
        actual = board.__repr__()
        self.assertEqual(expected,actual)

    def test_load_board_from_file(self):
        infile=open('test_data/sample_board0.txt','r')
        board=Board.create_board_from_text(infile.read())
        pieces = board.get_pieces(Color.WHITE)
        infile.close()
        self.assertEqual(len(pieces),1)
        self.assertTrue(isinstance(pieces[0],Queen))

    def test_successor_board(self):
        board=Board()
        board.new_game()
        move_pawn_up_1=Move(board,src=(1,0),dest=(2,0),color=Color.WHITE)
        successor=board.create_successor_board(move_pawn_up_1)
        #print(successor)
        self.assertTrue(successor.square_at(1,0).get_piece() is None)
        piece = successor.square_at(2,0).get_piece()
        self.assertIsInstance(piece,Pawn)
        self.assertEqual(piece.get_color(), Color.WHITE)

# def test_cli_board():
#     board=Board().new_game()


if __name__ == '__main__':
    unittest.main()
