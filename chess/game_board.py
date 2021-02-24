from chess.chess_piece import *
class Board:

    def __init__(self):
        self.grid = list()
        for r in range(0,8):
            self.grid.append(list())
            for c in range(0,8):
                is_white = (r+c%2==0) #color of space on board determined as such
                self.grid[r].append(GridSpace(is_white=is_white))

    def new_game(self):
        """Fills in pieces matching their position in a new game of chess"""
        for c in range(0,8):
            self.grid[1][c].add_piece(Pawn(is_white=True))
            self.grid[6][c].add_piece(Pawn(is_white=False))


    def get_pieces(self,color):
        """Returns all pieces belonging to the player indicated by color.
        The color parameter is a boolean variable--true for white, false for black"""

    def create_successor_board(self,move):
        """Returns a new game board, identical to this instance except one piece has been moved (as specified by the move
        parameter, which is an instance of the Move class.)
        Used by AI agent to determine effects of possible moves, as well is in checking whether the king is in check"""
        pass
    def square_at(self,row,col):
        """A method for returning a GridSpace based on numeric indexing"""
        return self.grid[row][col]

    def __repr__(self):
        """Returns a string representation of this board, used in command-line based gameplay"""
        pass

    @staticmethod
    def create_board_from_text(str):
        """Creates a board based off a string representation of a chess board. To be used in unit testing"""
        #TODO determine format for string representation of chess board



class GridSpace:
    def __init__(self,is_white,):
        self.color = is_white
    def is_empty(self):
        """Returns true if a piece is within this grid space, false otherwise"""
        return False
    def add_piece(self,piece):
        """Adds a piece to this position. Throws an exception if a piece is already present."""
        pass
    def get_piece(self):
        """Returns the current piece located on this square, or None if there is no piece here"""
    def remove_piece(self):
        """Removes the piece stored on the current grid square. Throws an exception if no piece is present"""
        pass