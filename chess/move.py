class Move:
    """
    A class to represent the act of moving a piece.
    """

    def __init__(self, board, src, dest, **kwargs):
        self.src = src
        self.dest = dest
        self.piece_moved = board.square_at(*src).get_piece()
        self.piece_captured = board.square_at(*dest).get_piece()
        # TODO add handling of special moves (e.g. check/checkmate, castling, pawn promotion)

    def __repr__(self):
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
    def create_move_from_str(board, str):
        """Creates a move based on standard algebraic notation for chess moves"""
