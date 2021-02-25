from chess.game_board import *
def test_empty_board():
    board = Board()
    pieces = board.get_pieces(True)
    assert len(pieces) == 0
    pieces = board.get_pieces(False)
    assert len(pieces) == 0

def test_new_board():
    board=Board()
    board.new_game()
    assert len(board.get_pieces(True))==16

    infile = open('test_data/new_board.txt','r')
    expected = infile.read()
    infile.close()
    actual = board.__repr__()
    assert expected == actual

def test_load_board_from_file():
    infile=open('test_data/sample_board0.txt','r')
    board=Board.create_board_from_text(infile.read())
    pieces = board.get_pieces(True)
    infile.close()
    assert len(pieces)==1
    assert isinstance(pieces[0][0],Queen)

def test_successor_board():
    board=Board()
    board.new_game()
    move_pawn_up_1=Move(board,src=(1,0),dest=(2,0))
    successor=board.create_successor_board(move_pawn_up_1)
    print(successor)
    assert successor.square_at(1,0).get_piece() is None
    piece = successor.square_at(2,0).get_piece()
    assert isinstance(piece,Pawn)
    assert piece.get_color()



test_new_board()
test_empty_board()
test_load_board_from_file()
