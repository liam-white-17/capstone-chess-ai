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
        return random.choice(board.get_all_moves(self.color))
