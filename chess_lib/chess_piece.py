import re
from abc import abstractmethod
from chess_lib.move import Move, Castle, PawnPromotion
from chess_lib.chess_utils import is_valid, is_capture, Color, is_check, convert_rank_file_to_int


class Piece:
    """
    Abstract class used to represent a piece on the game board
    """
    name = '*'
    has_moved = False

    def __init__(self, **kwargs):
        self.color = Color.WHITE if kwargs['is_white'] else Color.BLACK
        self.row = None
        self.col = None
        if 'loc' in kwargs:
            row, col = kwargs['loc']
            self.row = row
            self.col = col

    @abstractmethod
    def get_valid_moves(self, board, full_recursion=True):
        """Returns valid moves (and captures) on the board for this piece at the given grid location.
        Note that this does not take into account whether the move would put the current player's king in check"""
        return []

    def get_color(self):
        """Returns true if piece is on the white team, false if black"""
        return self.color

    def set_loc(self, loc):
        self.row, self.col = loc

    def __repr__(self):
        return self.to_char()

    def __str__(self):
        return self.to_char()

    def to_char(self):
        return self.name.upper() if self.color == Color.WHITE else self.name.lower()

    def to_unicode(self):
        return self.white_unicode if self.color else self.black_unicode

    def __eq__(self, other):
        return other.name == self.name and self.color == other.color and self.row == other.row and self.col == other.col

    def __deepcopy__(self, memodict={}):
        piece_type = get_piece_type_from_string(self.to_char())
        piece = piece_type(is_white=self.color, loc=(self.row, self.col))
        piece.has_moved = self.has_moved
        return piece
    def get_loc(self):
        return (self.row,self.col)

    @staticmethod
    def create_piece_from_string(str, color=None):
        if str == '*':
            return None
        return get_piece_type_from_string(str)(is_white=str.isupper())


class Pawn(Piece):
    name = 'P'
    white_unicode = '♙'
    black_unicode = '♟'

    def get_valid_moves(self, board, full_recursion=True):
        # Pawn moves for rules are different, making it difficult to use the is_valid method from util
        moves = []
        rank, file = self.row, self.col
        direction = 1 if self.color else -1
        origin_row = 1 if self.color else 6
        end_of_board = 7 if self.color else 0
        if is_valid(rank+direction,file,board,self.color) and not is_capture(rank+direction,file,board,self.color):
            moves.append(Move(board=board, src=(rank, file), dest=(rank + direction, file), color=self.color))
            if rank == origin_row and board.square_at(rank + (direction * 2), file).get_piece() is None:
                moves.append(Move(board=board, src=(rank, file), dest=(rank + direction * 2, file), color=self.color))
        if is_capture(rank + direction, file - 1, board, self.color):
            moves.append(Move(board=board, src=(rank, file), dest=(rank + direction, file - 1), color=self.color))
        if is_capture(rank + direction, file + 1, board, self.color):
            moves.append(Move(board=board, src=(rank, file), dest=(rank + direction, file + 1), color=self.color))
        final_moves = []
        piece_types = [Knight, Bishop, Queen, Rook]
        for move in moves:
            if move.dest[0] == end_of_board:
                for piece_type in piece_types:
                    final_moves.append(PawnPromotion(board=board, src=move.src, dest=move.dest, color=self.color,
                                                     new_piece_type=piece_type))
            else:
                final_moves.append(move)
        return final_moves


class Knight(Piece):
    name = 'H'
    white_unicode = '♘'
    black_unicode = '♞'

    def get_valid_moves(self, board, full_recursion=True):
        moves = []
        rank, file = self.row,self.col
        indices = [
            (rank + 2, file + 1),
            (rank + 2, file - 1),
            (rank - 2, file + 1),
            (rank - 2, file - 1),
            (rank + 1, file + 2),
            (rank + 1, file - 2),
            (rank - 1, file + 2),
            (rank - 1, file - 2)
        ]
        for r, f in indices:
            if is_valid(r, f, board, self.color):
                moves.append(Move(board=board, src=(rank, file), dest=(r, f), color=self.color))
        return moves


class Bishop(Piece):
    name = 'B'
    white_unicode = '♗'
    black_unicode = '♝'

    def get_valid_moves(self, board, full_recursion=True):

        return create_diagonal_moves(board, (self.row,self.col), self.color)


class Rook(Piece):
    name = 'R'
    white_unicode = '♖'
    black_unicode = '♜'

    def get_valid_moves(self, board, full_recursion=True):
        return create_orthogonal_moves(board, (self.row,self.col), self.color)


class Queen(Piece):
    name = 'Q'
    white_unicode = '♕'
    black_unicode = '♛'

    def get_valid_moves(self, board, full_recursion=True):
        return create_diagonal_moves(board, (self.row,self.col), self.color) +\
               create_orthogonal_moves(board, (self.row,self.col), self.color)


class King(Piece):
    name = 'K'
    white_unicode = '♔'
    black_unicode = '♚'

    def get_valid_moves(self, board, full_recursion=True):
        moves = []
        king_loc = (0,4) if self.color else (7,4)
        rank, file = self.row,self.col
        indices = [
            (rank + 1, file + 1),
            (rank + 1, file),
            (rank + 1, file - 1),
            (rank, file + 1),
            (rank, file - 1),
            (rank - 1, file + 1),
            (rank - 1, file),
            (rank - 1, file - 1)
        ]
        for r, f in indices:
            if is_valid(r, f, board, self.color):
                moves.append(Move(board=board, src=(rank, file), dest=(r, f), color=self.color))
        if not self.has_moved and full_recursion and (rank,file) == king_loc and not is_check(board, self.color):
            queenside_rook_loc = (0, 0) if self.color else (7, 0)
            kingside_rook_loc = (0, 7) if self.color else (7, 7)
            queenside_rook = board.piece_at(*queenside_rook_loc)
            kingside_rook = board.piece_at(*kingside_rook_loc)
            if queenside_rook is not None and not queenside_rook.has_moved:
                can_move_queenside = True
                for c in range(file - 1, 0, -1):
                    if board.piece_at(queenside_rook_loc[0], c) is not None:
                        can_move_queenside = False
                        break
                if can_move_queenside:
                    moves.append(Castle(board, self.color, is_queenside=True))
            if kingside_rook is not None and not kingside_rook.has_moved:
                can_move_kingside = True
                for c in range(file + 1, 7):
                    if board.piece_at(kingside_rook_loc[0], c) is not None:
                        can_move_kingside = False
                        break
                if can_move_kingside:
                    moves.append(Castle(board, self.color, is_queenside=False))

        return moves


def create_diagonal_moves(board, grid_loc, color):
    move_list = []
    rank, file = grid_loc[0] + 1, grid_loc[1] + 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        rank += 1
        file += 1
    rank, file = grid_loc[0] + 1, grid_loc[1] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        rank += 1
        file += -1
    rank, file = grid_loc[0] - 1, grid_loc[1] + 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        rank += -1
        file += 1
    rank, file = grid_loc[0] - 1, grid_loc[1] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        rank += -1
        file += -1
    return move_list


def create_orthogonal_moves(board, grid_loc, color):
    move_list = []
    rank, file = grid_loc[0], grid_loc[1] + 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        file += 1
    file = grid_loc[1] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        file += -1
    rank = grid_loc[0] + 1
    file = grid_loc[1]
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        rank += 1
    rank = grid_loc[0] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board, color=color))
        if is_capture(rank, file, board, color):
            break
        rank += -1
    return move_list


def get_piece_type_from_string(char):
    mydict = {'p': Pawn, 'h': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King, '*': None}
    return mydict[char.lower()]

def create_move_from_str(board, str:str,player_to_move):
    """Creates a move from a string that's (loosely) based on standard algebraic notation for chess_lib moves.
    This method has to be in this file to avoid a circular import"""
    if str in ['0-0','0-0-0']:
        loc = board.get_king_location(player_to_move)
        king = board.piece_at(*loc)
        moves = king.get_valid_moves(board)
        queenside = str == '0-0-0'
        can_castle = False
        for move in moves:
            if isinstance(move,Castle) and move.is_queenside == queenside:
                can_castle = True
                return move
        if not can_castle:
            raise ValueError('Board does not meet requirements for castling')

    regex = re.compile('[phbrqkPHBRQK][abcdefgh][1-8]x?[abcdefgh][1-8](=[hbrqHBRQ])?')
    if regex.fullmatch(str) is None:
        raise ValueError(f'{str} does not match accepted chess_lib notation')

    str = str.replace('x','')
    #expected_piece_type = get_piece_type_from_string(str[0])

    src = convert_rank_file_to_int(str[1:3])
    dest = convert_rank_file_to_int(str[3:5])
    pawn_regex = re.compile('=[hbrqHBRQ]')
    match = pawn_regex.match(str[-2:])
    if match is not None:
        return PawnPromotion(board,src,dest,player_to_move,new_piece_type=get_piece_type_from_string(str[-1]))
    return Move(board,src,dest,player_to_move)

