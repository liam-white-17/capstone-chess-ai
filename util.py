class Stack:
    """A container with a last-in-first-out (LIFO) queuing policy."""

    def __init__(self):
        self.list = []

    def push(self, item):
        """Push 'item' onto the stack"""
        self.list.append(item)

    def pop(self):
        """Pop the most recently pushed item from the stack"""
        return self.list.pop()

    def is_empty(self):
        """Returns true if the stack is empty"""
        return len(self.list) == 0
def is_valid(rank,file,board,color):
    """Returns true if a move to the position indicated by rank/file is valid.
    Valid in this case means within the bounds of the board and does not contain a piece of the same color
    """
    if rank < 0 or rank >= 8 or file < 0 or file >= 8:
        return False
    piece = board.square_at(rank, file).get_piece()
    return piece is None or piece.get_color() != color

def is_capture(rank,file,board,color):
    if not is_valid(rank,file,board,color):
        return False
    piece = board.square_at(rank,file).get_piece()
    return piece is not None and piece.get_color() != color


