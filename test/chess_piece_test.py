from chess.chess_piece import *
from chess.game_board import Board
from chess.move import Move

def test_pawn_moves():
    board = Board()
    board.new_game()
    white_pawn = board.square_at(1,0).get_piece()
    black_pawn = board.square_at(6,0).get_piece()
    assert white_pawn is not None
    assert black_pawn is not None
    white_pawn_moves = white_pawn.get_valid_moves(board,(1,0))
    black_pawn_moves = black_pawn.get_valid_moves(board,(6,0))
    white_move_1_square = Move(src=(1,0),dest=(2,0),board=board,color=Color.WHITE)
    white_move_2_squares = Move(src=(1,0),dest=(3,0),board=board,color=Color.WHITE)
    expected = white_move_1_square
    actual = white_pawn_moves[0]
    assert expected == actual
    expected = white_move_2_squares
    actual = white_pawn_moves[1]
    assert expected == actual
    black_move_1_square = Move(src=(6, 0), dest=(5, 0), board=board,color=Color.WHITE)
    expected = black_move_1_square
    actual = black_pawn_moves[0]
    assert expected == actual

def test_knight_moves():
    board=Board()
    board.new_game()
    white_horse = board.square_at(0,1).get_piece()
    moves = white_horse.get_valid_moves(board,(0,1))
    assert Move(src=(0,1),dest=(2,0),board=board,color=Color.WHITE) in moves
    assert Move(src=(0,1),dest=(2,2),board=board,color=Color.WHITE) in moves

def test_queen_moves():
    #there is no reason why bishop/rook moves won't work if queen moves work, so we skip ahead in testing
    board=Board.load_from_file('test_data/sample_board0.txt')
    queen=board.square_at(3,2).get_piece()
    moves = queen.get_valid_moves(board,(3,2))
    assert Move(src=(3,2),dest=(4,3),board=board,color=Color.WHITE) in moves
    assert Move(src=(3,2),dest=(2,3),board=board,color=Color.WHITE) in moves
    assert Move(src=(3,2),dest=(3,7),board=board,color=Color.WHITE) in moves
    assert Move(src=(3,2),dest=(0,2),board=board,color=Color.WHITE) in moves
    assert Move(src=(3,2),dest=(0,0),board=board,color=Color.WHITE) not in moves

def test_king_moves():
    board=Board.load_from_file('test_data/sample_board1.txt')
    king=board.square_at(0,1).get_piece()
    moves = king.get_valid_moves(board,(0,1))
    assert len(moves) == 5
    assert Move(src=(0,1),dest=(0,0),board=board,color=Color.WHITE) in moves
    assert Move(src=(0,1),dest=(1,2),board=board,color=Color.WHITE) in moves
    assert Move(src=(0,1),dest=(1,1),board=board,color=Color.WHITE) in moves







test_pawn_moves()
test_knight_moves()
test_queen_moves()
test_king_moves()