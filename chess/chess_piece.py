from abc import abstractmethod


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
        #TODO
        return None


class Knight(Piece):
    name = 'H'
    def get_valid_moves(self,board,grid_loc):
        #TODO
        return None


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


