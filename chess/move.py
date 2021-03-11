import re
from chess.chess_utils import *

class Move:
    """
    A class to represent the act of moving a piece.
    """

    def __init__(self, board, src, dest, color, **kwargs):
        self.src = src
        self.dest = dest
        self.piece_moved = board.square_at(*src).get_piece()
        self.piece_captured = board.square_at(*dest).get_piece()
        self.color = color
        # TODO add handling of special moves (e.g. check/checkmate, castling, pawn promotion)

    def __repr__(self):
        out = f'{self.piece_moved}{convert_int_to_rank_file(self.src)}'
        out += ('x' if self.piece_captured is not None else '')
        out += f'{convert_int_to_rank_file(self.dest)}'
        return out


    def grid_repr(self):
        output = f'{self.piece_moved}{self.src}==>{self.dest}'
        if self.piece_captured is not None:
            output += f'x{self.piece_captured}'
        return output

    def __eq__(self, other):
        return self.src == other.src and \
               self.dest == other.dest and \
               self.piece_moved == other.piece_moved and \
               self.piece_captured == other.piece_captured

    @staticmethod
    def create_move_from_board(board, src, dst):
        """Creates a instance of the move class based on an existing board with source/destination coordinates"""""
        pass

    @staticmethod
    def create_move_from_str(board, str:str,player_to_move):
        """Creates a move from a string that's (loosely) based on standard algebraic notation for chess moves"""
        regex = re.compile('[phbrqkPHBRQK][abcdefgh][1-8]x?[abcdefgh][1-8]')
        if regex.fullmatch(str) is None:
            raise ValueError(f'{str} does not match accepted chess notation')

        str.replace('x','')
        #expected_piece_type = get_piece_type_from_string(str[0])

        src = convert_rank_file_to_int(str[1:3])
        dest = convert_rank_file_to_int(str[3:5])
        #actual_piece = board.square_at(src).get_piece()
        # if not isinstance(actual_piece,expected_piece_type):
        #     raise ValueError(f'Piece at {convert_int_to_rank_file(src)} is not of type {expected_piece_type}')
        return Move(board,src,dest,player_to_move)

class Castle(Move):

    def __init__(self,board,color,is_queenside):
        queenside_rook_loc = (0, 0) if color else (7, 0)
        kingside_rook_loc = (0, 7) if color else (7, 7)
        king_loc = (0,4) if color else (7,4)
        new_king_loc = (king_loc[0],king_loc[1]+(2 if is_queenside else -2))
        Move.__init__(self,board,src=king_loc,dest=new_king_loc,color=color)
        self.is_queenside = is_queenside
        self.rook_src = queenside_rook_loc if is_queenside else kingside_rook_loc
        self.rook_dest = (self.rook_src[0],self.rook_src[1]+(-2 if is_queenside else 2))

    def __repr__(self):
        return '0-0-0' if self.is_queenside else '0-0'



