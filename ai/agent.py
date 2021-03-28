from abc import abstractmethod
import random

from chess_lib.chess_utils import is_check,is_checkmate,no_valid_moves,Color

class Agent:
    """A chess_lib-playing AI agent"""
    def __init__(self,**args):
       self.color = args['color']
    @abstractmethod
    def get_next_move(self,board):
        return None

class RandomAgent(Agent):
    """Picks next move from randomly available options"""
    def __init__(self,**args):
        Agent.__init__(self,**args)

    def get_next_move(self,board,no_moves_to_check=True):
        moves = board.get_all_moves(self.color,no_moves_to_check=no_moves_to_check)
        return random.choice(moves)
class FixedRandomAgent(RandomAgent):
    """Similar to RandomAgent except the move chosen will be the same every time (assuming identical conditions).
    This is used in analysis of an AI agent to ensure that any two AI agents are playing against the 'same' player."""
    def __init__(self,**args):
        RandomAgent.__init__(self,**args)
        random.seed(args['seed'] if 'seed' in args else 7)
