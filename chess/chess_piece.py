from abc import abstractmethod
from chess.move import Move
from util import is_valid,is_capture
class Piece:
    """
    NOT IMPLEMENTED
    Abstract class used to represent a piece on the game board
    """
    name = '*'
    def __init__(self,**kwargs):
        self.color = kwargs['is_white']

        pass

    @abstractmethod
    def get_valid_moves(self,board,grid_loc):
        """Returns valid moves (and captures) on the board for this piece at the given grid location.
        Note that this does not take into account whether the move would put the current player's king in check"""
        return []

    def get_color(self):
        """Returns true if piece is on the white team, false if black"""
        return self.color
    def __repr__(self):
        return self.name.upper() if self.color else self.name.lower()

class Pawn(Piece):
    name = 'P'
    def get_valid_moves(self,board,grid_loc):
        #Pawn moves for rules are different
        moves = []
        rank,file=grid_loc
        direction = 1 if self.color else -1
        origin_row = 1 if self.color else 6
        if board.square_at(rank+direction,file).get_piece() is None:
            moves.append(Move(board=board,src=(rank,file),dest=(rank+direction,file)))
            if rank == origin_row and board.square_at(rank+(direction*2),file).get_piece() is None:
                moves.append((Move(board=board,src=(rank,file),dest=(rank+direction*2,file))))
        if is_capture(rank+direction,file-1,board,self.color):
            moves.append(Move(board=board,src=(rank,file),dest=(rank+direction,file-1)))
        if is_capture((rank+direction,file+1,board,self.color)):
            moves.append(Move(board=board,src=(rank,file),dest=(rank+direction,file-1)))
        return moves



class Knight(Piece):
    name = 'H'
    def get_valid_moves(self,board,grid_loc):
        #TODO
        moves=[]
        rank,file=grid_loc
        indices=[
            (rank+2,file+1),
            (rank+2,file-1),
            (rank-2,file+1),
            (rank-2,file-1),
            (rank+1,file+2),
            (rank+1,file-2),
            (rank-1,file+2),
            (rank-1,file-2)
        ]
        for r,f in indices:
            if is_valid(r,f,board,self.color):
                moves.append(Move(board=board,src=(rank,file),dest=(r,f)))
        return moves


class Bishop(Piece):
    name='B'
    def get_valid_moves(self,board,grid_loc):
        #TODO
        return None

class Rook(Piece):
    name='R'
    def get_valid_moves(self,board,grid_loc):
        #TODO
        return None

class Queen(Piece):
    name='Q'
    def get_valid_moves(self,board,grid_loc):
        #TODO
        return None

class King(Piece):
    name = 'K'
    def get_valid_moves(self,board,grid_loc):
        #TODO
        return None


