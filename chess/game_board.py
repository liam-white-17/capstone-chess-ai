from chess.chess_piece import *
import io,copy


class Board:

    def __init__(self):
        self.grid = list()
        for r in range(0, 8):
            self.grid.append(list())
            for c in range(0, 8):
                self.grid[r].append(GridSpace((r, c)))

    def new_game(self):
        """Fills in pieces matching their position in a new game of chess"""
        for c in range(0, 8):
            self.grid[1][c].add_piece(Pawn(is_white=True))
            self.grid[6][c].add_piece(Pawn(is_white=False))
        self.grid[0][0].add_piece(Rook(is_white=True))
        self.grid[0][7].add_piece(Rook(is_white=True))
        self.grid[7][0].add_piece(Rook(is_white=False))
        self.grid[7][7].add_piece(Rook(is_white=False))
        self.grid[0][1].add_piece(Knight(is_white=True))
        self.grid[0][6].add_piece(Knight(is_white=True))
        self.grid[7][1].add_piece(Knight(is_white=False))
        self.grid[7][6].add_piece(Knight(is_white=False))
        self.grid[0][2].add_piece(Bishop(is_white=True))
        self.grid[0][5].add_piece(Bishop(is_white=True))
        self.grid[7][2].add_piece(Bishop(is_white=False))
        self.grid[7][5].add_piece(Bishop(is_white=False))
        self.grid[0][3].add_piece(Queen(is_white=True))
        self.grid[0][4].add_piece(King(is_white=True))
        self.grid[7][4].add_piece(Queen(is_white=False))
        self.grid[7][3].add_piece(King(is_white=False))

    def get_pieces(self, color):
        """Returns all the pieces of a given color.
        Pieces are stored in tuples containing the piece and their coordinates.
        The color parameter is a boolean variable--true for white, false for black"""
        pieces = []
        for rank in range(0, 8):
            for file in range(0, 8):
                piece = self.grid[rank][file].get_piece()
                if piece is not None and piece.get_color() == color:
                    pieces.append((piece, (rank, file)))
        return pieces

    def create_successor_board(self, move):
        """Returns a new game board, identical to this instance except one piece has been moved (as specified by the move
        parameter, which is an instance of the Move class.)
        Used by AI agent to determine effects of possible moves, as well as in checking whether the king is in check"""
        temp=self
        src,dest=move.src,move.dest
        temp.square_at(*src).remove_piece()
        if not temp.square_at(*dest).is_empty():
            temp.square_at(*dest).remove_piece()
        temp.square_at(*dest).add_piece(move.piece_moved)
        return temp


    def square_at(self, row, col):
        """A method for returning a GridSpace based on numeric indexing"""
        return self.grid[row][col]

    def __repr__(self):
        """Returns a string representation of this board, used in command-line based gameplay"""
        output = ""
        for rank in range(7, -1, -1):
            row = ""
            for file in range(0, 8):
                piece = self.grid[rank][file].get_piece()
                row += ' ' + ('*' if piece is None else piece.to_char())
            output += '\n' + row.lstrip(' ')
        return output.lstrip('\n')

    @staticmethod
    def load_from_file(fpath):
        "Loads a board from a file"
        infile = open(fpath)
        input = infile.read()
        return Board.create_board_from_text(input)

    @staticmethod
    def create_board_from_text(char_grid):
        """Creates a board based off a string representation of a chess board. To be used in testing"""
        board = Board()
        char_rows = char_grid.split('\n')
        if len(char_rows) != 8:
            raise Exception("Bad input for loading board from text; input recieved:\n" + char_grid)
        for rank in range(0, 8):
            curr_row = char_rows[rank].split(' ')
            for file in range(0, 8):
                chr = curr_row[file]
                piece_type = get_piece_type_from_string(chr)
                if piece_type is not None:
                    board.grid[7 - rank][file].add_piece(piece_type(is_white=(chr == chr.upper())))
        return board


class GridSpace:
    def __init__(self, loc):
        r, c = loc
        self.loc = loc
        self.color = (r + c % 2 == 0)  # color of space on board determined as such
        self.piece = None

    def is_empty(self):
        """Returns true if no piece is within this grid space, false otherwise"""
        return self.piece is None

    def add_piece(self, piece):
        """Adds a piece to this position. Throws an exception if a piece is already present."""
        if self.piece is not None:
            raise ValueError(f'Cannot add piece {piece} to {self.loc} because {self.piece} is already present')
        self.piece = piece

    def get_piece(self):
        """Returns the current piece located on this square, or None if there is no piece here"""
        return self.piece

    def set_piece(self,piece):
        """Replaces current piece (if present) with the piece parameter.
        Although this method essentially combines the effects of add_piece and remove_piece, it's better practice
        to use one of the others as"""

    def remove_piece(self):
        """Removes the piece stored on the current grid square. Throws an exception if no piece is present"""
        if self.piece is None:
            raise ValueError(f'No piece to remove from {self.loc}!')
        piece = self.piece
        self.piece = None
        return piece
