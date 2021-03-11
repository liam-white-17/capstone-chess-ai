from abc import abstractmethod
import random

from chess.chess_utils import is_check,is_checkmate,no_valid_moves,Color

class Agent:
    """A chess-playing AI agent"""
    def __init__(self,**args):
       self.color = args['color']
    @abstractmethod
    def get_next_move(self,board):
        return None

class RandomAgent(Agent):
    """Picks next move from randomly available options"""

    def get_next_move(self,board):
        pieces = board.get_pieces(self.color)
        valid_moves = []
        for piece, loc in pieces:
            for move in piece.get_valid_moves(board,loc):
                successor = board.create_successor_board(move)
                if not is_check(successor,self.color):
                    valid_moves.append(move)
        return random.choice(valid_moves)
