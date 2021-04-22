from chess_lib.chess_piece import *
from colorama import init as colorama_init, deinit as colorama_deinit,Fore,Back,Style

EMPTY_SQUARE_NO_UNICODE = '   '
EMPTY_SQUARE_UNICODE = '   \u205f'
WHITE_PIECE_ANSI = Fore.WHITE + Style.BRIGHT
BLACK_PIECE_ANSI = Fore.BLACK
class Board:
    def __init__(self,dim=8):
        """Constructor"""
        self.grid = list()
        self.dim = dim
        # self.grid = ([[GridSpace((r,c)) for r in range(0,8)] for c in range(0,8)])
        for r in range(0, dim):
            self.grid.append(list())
            for c in range(0, dim):
                self.grid[r].append(GridSpace((r, c)))
        # print(self.grid)
        self.white_pieces = []
        self.black_pieces = []

    def new_game(self):
        """Fills in pieces matching their position in a new game of chess_lib"""
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
        self.grid[7][3].add_piece(Queen(is_white=False))
        self.grid[7][4].add_piece(King(is_white=False))

        self.set_piece_locations()
        return self

    def set_piece_locations(self):
        """Helper function"""
        for rank in range(0,8):
            for file in range(0,8):
                piece = self.piece_at(rank,file)
                if piece is None:
                    continue
                if piece.color == Color.WHITE:
                    self.white_pieces.append(piece)
                else:
                    self.black_pieces.append(piece)
    def get_pieces(self,color):
        return self.white_pieces if color else self.black_pieces


    def create_successor_board(self, move):
        """Returns a new game board, identical to this instance except one piece has been moved (as specified by the move
        parameter, which is an instance of the Move class.)
        Used by AI agent to determine effects of possible moves, as well as in checking whether the king is in check.
        This method does not check the validity of any moves passed to it (that is handled outside of this method)."""
        temp=self.__deepcopy__()
        src,dest=move.src,move.dest
        #temp.square_at(*src).remove_piece()
        if not temp.square_at(*dest).is_empty():
            piece_to_remove = temp.square_at(*dest).remove_piece().__deepcopy__()
            if piece_to_remove.color == Color.WHITE:
                temp.white_pieces.remove(piece_to_remove)
            else:
                temp.black_pieces.remove(piece_to_remove)
        piece_to_move = temp.square_at(*src).remove_piece()
        if piece_to_move.color == Color.WHITE:
            temp.white_pieces.remove(piece_to_move)
        else:
            temp.black_pieces.remove(piece_to_move)

        piece_to_move.has_moved = True
        temp.square_at(*dest).add_piece(piece_to_move)

        if isinstance(move,Castle):
            rook_src, rook_dest = move.rook_src,move.rook_dest
            rook = temp.square_at(*rook_src).remove_piece()
            if rook.color == Color.WHITE:
                temp.white_pieces.remove(rook)
                temp.white_pieces.append(temp.piece_at(*dest))
            else:
                temp.black_pieces.remove(rook)
                temp.black_pieces.append(temp.piece_at(*dest))
            temp.square_at(*rook_dest).add_piece(rook)
            if rook.color == Color.WHITE:
                temp.white_pieces.append(temp.piece_at(*rook_dest))
            else:
                temp.black_pieces.append(temp.piece_at(*rook_dest))
        elif isinstance(move,PawnPromotion):
            temp.square_at(*dest).remove_piece()
            new_piece = move.new_piece.__deepcopy__()
            temp.square_at(*dest).add_piece(move.new_piece)
            if new_piece.color == Color.WHITE:
                temp.white_pieces.append(temp.piece_at(*dest))
            else:
                temp.black_pieces.append(temp.piece_at(*dest))
        else:
            if piece_to_move.color == Color.WHITE:
                temp.white_pieces.append(temp.square_at(*dest).get_piece())
            else:
                temp.black_pieces.append(temp.square_at(*dest).get_piece())

        return temp
    def get_king_location(self,color):
        # return self.white_king.get_loc() if color == Color.WHITE else self.black_king.get_loc()
        # # for r in range(0,8):
        # #     for c in range(0,8):
        # #         piece = self[(r,c)].get_piece()
        # #         if piece is not None and piece.get_color() == color and isinstance(piece,King):
        # #             return (r,c)
        # # raise Exception("Cannot find King!")
        piece_list = self.white_pieces if color else self.black_pieces
        for piece in piece_list:
            if isinstance(piece, King):
                return (piece.row, piece.col)
        raise ValueError('Cannot Find King!')

    def __getitem__(self, item):
        return self.grid[item[0]][item[1]]
    def square_at(self, row, col):
        """A method for returning a GridSpace based on numeric indexing"""
        return self.grid[row][col]
    def get_all_moves(self,color,no_moves_to_check=True,full_recursion=True):
        #full recursion is set to false when evaluating a castling move to avoid an infinite loop
        all_moves = []
        pieces = self.get_pieces(color)
        for piece in pieces:
            curr_moves = piece.get_valid_moves(self,full_recursion=full_recursion)
            for move in curr_moves:
                successor = self.create_successor_board(move)
                if not no_moves_to_check or not is_check(successor, color):
                    all_moves.append(move)
        return all_moves
    def __eq__(self, other):
        if not isinstance(other,Board):
            return False
        for r in range(0,8):
            for c in range(0,8):
                if self[(r,c)] != other[(r,c)]:
                    return False
        return True

    def piece_at(self,row,col):
        return self.grid[row][col].get_piece()
    def __repr__(self):
        """Returns a string representation of this board"""
        output = ""
        for row in range(7, -1, -1):
            board_row = ""
            for col in range(0, 8):
                piece = self.grid[row][col].get_piece()
                board_row += ' ' + ('*' if piece is None else piece.to_char())
            output += '\n' + board_row.lstrip(' ')
        return output.lstrip('\n')
    def display_board(self,unicode=False):
        """Displays board in standard chess_lib format (i.e. with ranks and files) as opposed to the (x,y) coordinate system
        used in implementation. This is used in the CLI output format of the game"""
        colorama_init(autoreset=True)
        separator = '  \u2005' if unicode else '  '
        header = separator.join(['a','b','c','d','e','f','g','h'])
        output = '   '+header
        for row in range(7, -1, -1):
            output_row = str(row+1)+' '
            for col in range(0, 8):
                # piece = self.grid[row][col].get_piece()
                # output_row += '  '  + ('*' if piece is None else (piece.to_char() if chars_only else piece.to_color_char()))
                output_row += self.grid[row][col].get_ui_output(unicode=unicode)
            output += Style.RESET_ALL+'\n' + output_row.lstrip(' ')
        output = output.lstrip('\n')
        print(output)
        colorama_deinit()
    @staticmethod
    def load_from_file(fpath):
        """Loads a board from a file, used in testing"""
        infile = open(fpath)
        input = infile.read()
        infile.close()
        return Board.create_board_from_text(input)

    @staticmethod
    def create_board_from_text(char_grid):
        """Creates a board based off a string representation of a chess_lib board. To be used in testing"""
        board = Board()
        char_rows = char_grid.split('\n')
        if len(char_rows) != 8:
            raise Exception("Bad input for loading board from text; input recieved:\n" + char_grid)
        for rank in range(0, 8):
            curr_row = char_rows[rank].replace('  ',' ').split(' ')
            for file in range(0, 8):
                chr = curr_row[file]
                piece_type = get_piece_type_from_string(chr)
                if piece_type is not None:
                    board.grid[7 - rank][file].add_piece(piece_type(is_white=(chr == chr.upper()),loc=(7-rank,file)))
                # if piece_type == King:
                #     color = Color.WHITE if chr.isupper() else Color.BLACK
                #     #board.king_locations[color] = (7-rank,file)
        board.set_piece_locations()
        return board
    def __deepcopy__(self, memodict={}):
        """As titled; creates deep copy of the chess_lib board"""
        board = Board()
        for row in range(0,8):
            for col in range(0,8):
                piece = self.square_at(row,col).get_piece()
                board.square_at(row,col).add_piece(piece.__deepcopy__() if piece is not None else None)
        # board.king_locations[Color.WHITE] = self.king_locations[Color.WHITE]
        # board.king_locations[Color.BLACK] = self.king_locations[Color.BLACK]
        board.white_pieces = [piece.__deepcopy__() for piece in self.white_pieces]
        board.black_pieces = [piece.__deepcopy__() for piece in self.black_pieces]

        return board


class GridSpace:
    """A class used to represent a cell on the chess_lib board. Though not particularly useful now, this class is implemented
    for UI considerations"""
    def __init__(self, loc):
        r, c = loc
        self.loc = loc
        self.color = ((r + c) % 2 == 0)  # color of space on board determined as such
        # note that for GridSpace, self.color represents the color of the SQUARE, which is purely for UI considerations.
        # it has no bearing on player/piece colors
        self.piece = None

    def __repr__(self):
        return '*' if self.piece is None else self.piece.to_char()
    def is_empty(self):
        """Returns true if no piece is within this grid space, false otherwise"""
        return self.piece is None
    def get_ui_output(self,unicode=False):
        background_color = (Back.YELLOW if self.color else Back.RED)  # yellow is used for white/beige squares, red for black/maroon squares

        if self.piece is None:
            return background_color + (EMPTY_SQUARE_UNICODE if unicode else EMPTY_SQUARE_NO_UNICODE)
        else:
            # if unicode:
            #     return background_color + self.piece.to_unicode()
            # else:
            foreground_color = WHITE_PIECE_ANSI if self.piece.color else BLACK_PIECE_ANSI
            piece_char = ('\u2005\u200A'+self.piece.to_unicode() + '\u2004\u200A') if unicode else f' {self.piece.to_char()} '
            return background_color + foreground_color + piece_char
            # piece_char = self.piece.to_unicode() if unicode else f' {self.piece.to_char()} '
            # return background_color + foreground_color + piece_char
    def add_piece(self, piece):
        """Adds a piece to this position. Throws an exception if a piece is already present."""
        if self.piece is not None:
            raise ValueError(f'Cannot add piece {piece} to {self.loc} because {self.piece} is already present')
        if piece is None:
            return
        self.piece = piece
        self.piece.set_loc(self.loc)

    def get_piece(self):
        """Returns the current piece located on this square, or None if there is no piece here"""
        return self.piece

    def remove_piece(self):
        """Removes the piece stored on the current grid square. Throws an exception if no piece is present"""
        if self.piece is None:
            raise ValueError(f'No piece to remove from {self.loc}!')
        piece = self.piece.__deepcopy__()
        self.piece = None
        return piece
    def __eq__(self, other):
        if not isinstance(other,GridSpace):
            return False
        if self.piece is None or other.piece is None:
            return self.piece is None and other.piece is None
        return self.piece == other.piece
