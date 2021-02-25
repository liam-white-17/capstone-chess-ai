from abc import abstractmethod
from chess.move import Move
from util import is_valid, is_capture


class Piece:
    """
    NOT IMPLEMENTED
    Abstract class used to represent a piece on the game board
    """
    name = '*'
    has_moved = False

    def __init__(self, **kwargs):
        self.color = kwargs['is_white']

        pass

    @abstractmethod
    def get_valid_moves(self, board, grid_loc):
        """Returns valid moves (and captures) on the board for this piece at the given grid location.
        Note that this does not take into account whether the move would put the current player's king in check"""
        return []

    def get_color(self):
        """Returns true if piece is on the white team, false if black"""
        return self.color

    def __repr__(self):
        return self.to_char()

    def __str__(self):
        return self.to_char()

    def to_char(self):
        return self.name.upper() if self.color else self.name.lower()
    def __eq__(self, other):
        return other.name == self.name and self.color == other.color


class Pawn(Piece):
    name = 'P'

    def get_valid_moves(self, board, grid_loc):
        # Pawn moves for rules are different, making it difficult to use the is_valid method from util
        moves = []
        rank, file = grid_loc
        direction = 1 if self.color else -1
        origin_row = 1 if self.color else 6
        if board.square_at(rank + direction, file).get_piece() is None:
            moves.append(Move(board=board, src=(rank, file), dest=(rank + direction, file)))
            if rank == origin_row and board.square_at(rank + (direction * 2), file).get_piece() is None:
                moves.append((Move(board=board, src=(rank, file), dest=(rank + direction * 2, file))))
        if is_capture(rank + direction, file - 1, board, self.color):
            moves.append(Move(board=board, src=(rank, file), dest=(rank + direction, file - 1)))
        if is_capture(rank + direction, file + 1, board, self.color):
            moves.append(Move(board=board, src=(rank, file), dest=(rank + direction, file - 1)))
        return moves


class Knight(Piece):
    name = 'H'

    def get_valid_moves(self, board, grid_loc):
        # TODO
        moves = []
        rank, file = grid_loc
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
                moves.append(Move(board=board, src=(rank, file), dest=(r, f)))
        return moves


class Bishop(Piece):
    name = 'B'

    def get_valid_moves(self, board, grid_loc):
        return create_diagonal_moves(board, grid_loc, self.color)


class Rook(Piece):
    name = 'R'

    def get_valid_moves(self, board, grid_loc):
        return create_orthogonal_moves(board, grid_loc, self.color)


class Queen(Piece):
    name = 'Q'

    def get_valid_moves(self, board, grid_loc):
        return create_diagonal_moves(board, grid_loc, self.color) + create_orthogonal_moves(board, grid_loc, self.color)


class King(Piece):
    name = 'K'

    def get_valid_moves(self, board, grid_loc):
        moves = []
        rank, file = grid_loc
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
                moves.append(Move(board=board, src=(rank, file), dest=(r, f)))
        return moves


def create_diagonal_moves(board, grid_loc, color):
    move_list = []
    rank, file = grid_loc[0] + 1, grid_loc[1] + 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        rank += 1
        file += 1
    rank, file = grid_loc[0] + 1, grid_loc[1] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        rank += 1
        file += -1
    rank, file = grid_loc[0] - 1, grid_loc[1] + 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        rank += -1
        file += 1
    rank, file = grid_loc[0] - 1, grid_loc[1] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        rank += -1
        file += -1
    return move_list


def create_orthogonal_moves(board, grid_loc, color):
    move_list = []
    rank, file = grid_loc[0], grid_loc[1] + 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        file += 1
    file = grid_loc[1] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        file += -1
    rank = grid_loc[0] + 1
    file = grid_loc[1]
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        rank += 1
    rank = grid_loc[0] - 1
    while is_valid(rank, file, board, color):
        move_list.append(Move(src=grid_loc, dest=(rank, file), board=board))
        if is_capture(rank, file, board, color):
            break
        rank += -1
    return move_list


def get_piece_type_from_string(char):
    mydict = {'p': Pawn, 'h': Knight, 'b': Bishop, 'q': Queen, 'k': King,'*':None}
    return mydict[char.lower()]
