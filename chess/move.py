class Move:
    """
    A class to represent the act of moving a piece.
    """
    def __init__(self,board,src,dest):
        self.src=src
        self.dest=dest
        self.piece_moved = board.square_at(*src).get_piece()
        self.piece_captured = board.square_at(*dest).get_piece()
        pass

    def __repr__(self):
        pass

    @staticmethod
    def create_move_from_board(board,src,dst):
        """Creates a instance of the move class based on an existing board with source/destination coordinates"""""
        pass

    @staticmethod
    def create_move_from_str(board,str):
        """Creates a move based on standard algebraic notation for chess moves"""
