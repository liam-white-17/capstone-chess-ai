from enum import Enum
class Color(Enum):
    """Represents the colors of pieces on the board and the corresponding player who controls them"""

    WHITE=True
    BLACK=False
    def __str__(self):
        return 'WHITE' if self == Color.WHITE else 'BLACK'
    def __bool__(self):
        return True if self == Color.WHITE else False
    def __invert__(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE


def is_valid(rank,file,board,color):
    """Returns true if a move to the position indicated by rank/file is valid.
    Valid in this case means within the bounds of the board and does not contain a piece of the same color
    """
    if rank < 0 or rank >= 8 or file < 0 or file >= 8:
        return False
    piece = board.square_at(rank, file).get_piece()
    return piece is None or piece.get_color() != color

def is_capture(rank,file,board,color):
    if not is_valid(rank,file,board,color):
        return False
    piece = board.square_at(rank,file).get_piece()
    return piece is not None and piece.get_color() != color

def convert_rank_file_to_int(rank_file):
    rank,file=int(rank_file[1]),rank_file[0]
    if rank < 1 or rank > 8:
        raise ValueError(f'rank of {rank} outside of legal values (1,2...8)')
    row = rank-1
    file_mapping = 'abcdefgh'
    if file not in file_mapping:
        raise ValueError(f'file of {file} outside of legal values (a,b...h)')
    col = file_mapping.index(file)
    return (row,col)

def convert_int_to_rank_file(loc):
    row,col=loc
    rank=row+1
    file_mapping='abcdefgh'
    file=file_mapping[col]
    return file+str(rank)


def is_check(board,player_to_move):
    pieces = board.get_pieces(~player_to_move)
    king_loc = board.get_king_location(player_to_move)
    # moves = board.get_all_moves(~player_to_move,no_moves_to_check=False,full_recursion=False)
    # for move in moves:
    #     if move.dest == king_loc:
    #         return True
    # return False
    for piece in pieces:
        for move in piece.get_valid_moves(board,full_recursion=False):
            if move.dest == king_loc:
                return True
    return False
def is_checkmate(board,player_to_move):
    return is_check(board,player_to_move) and no_valid_moves(board,player_to_move)

def is_stalemate(board,player_to_move):
    if len(board.get_pieces(player_to_move)) == 1 and len(board.get_pieces(~player_to_move)) == 1:
        return True
    return no_valid_moves(board,player_to_move) and not is_check(board,player_to_move)
def no_valid_moves(board,player_to_move):
    pieces = board.get_pieces(player_to_move)
    # return len(board.get_all_moves(player_to_move,no_moves_to_check=True,full_recursion=True)) == 0
    for piece in pieces:
        for move in piece.get_valid_moves(board):
            successor = board.create_successor_board(move)
            if not is_check(successor,player_to_move):
                return False
    return True
