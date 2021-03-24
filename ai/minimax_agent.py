from abc import abstractmethod
import time
from chess.chess_utils import *
from chess.chess_piece import *

from ai.agent import Agent
import math
class AbstractMinimaxAgent(Agent):
    """Abstract minimax agent that all minimax agents use as a superclass"""
    DEFAULT_MAX_DEPTH = 2 # depth increases each time min value is called from within max value or vice versa
    # for best resut
    STALEMATE_VAL = 0
    WIN_VAL = math.inf
    LOSE_VAL = -math.inf
    def __init__(self,**args):
        Agent.__init__(self,**args)
        self.max_depth = args['depth'] if 'depth' in args else self.DEFAULT_MAX_DEPTH
    def get_next_move(self,board):
        alpha0 = -math.inf
        beta0 = math.inf
        alpha = alpha0
        beta = beta0
        value = -math.inf
        best_move = None
        moves = board.get_all_moves(self.color)
        start = time.time()
        for curr_move in moves:
            successor = board.create_successor_board(curr_move)
            score = self.min_value(successor,curr_depth=0,alpha=alpha,beta=beta)
            if score > value:
                value = score
                best_move = curr_move
            if score > beta:
                return best_move
            alpha = max(alpha,value)
        stop = time.time()
        delta = stop-start
        print(f'Time to find move: {delta}')
        return best_move
    def min_value(self,state,curr_depth,alpha,beta):
        #print(f'Depth = {curr_depth}')
        if self.is_win(state):
            return self.WIN_VAL
        if self.is_lose(state):
            return self.LOSE_VAL
        if self.is_tie(state):
            return self.STALEMATE_VAL
        if curr_depth == self.max_depth:
            score = self.evaluation_function(state)
            #print(f'Depth = {curr_depth} score = {score}')
            return score
        val = math.inf
        moves = state.get_all_moves(~self.color)
        for move in moves:
            successor = state.create_successor_board(move)
            score = self.max_value(successor,curr_depth+1,alpha,beta)
            val = min(val,score)
            if val < alpha:
                return val
        return val

    def max_value(self,state,curr_depth,alpha,beta):
        if self.is_win(state):
            return self.WIN_VAL
        if self.is_lose(state):
            return self.LOSE_VAL
        if self.is_tie(state):
            return self.STALEMATE_VAL
        if curr_depth == self.max_depth:
            score = self.evaluation_function(state)
            #print(f'Depth = {curr_depth} score = {score}')
            return score
        val = -math.inf
        moves = state.get_all_moves(self.color)
        for move in moves:
            successor = state.create_successor_board(move)
            score = self.min_value(successor,curr_depth+1,alpha,beta)
            val = max(val,score)
            if val > beta:
                return val
            alpha = max(alpha,val)
        return val

    def is_win(self,board):
        return is_checkmate(board,self.color)
    def is_lose(self,board):
        return is_checkmate(board,~self.color)
    def is_tie(self,board):
        return no_valid_moves(board,self.color) and not is_check(board,self.color)


    @abstractmethod
    def evaluation_function(self,state):
        pass

class PieceValueAgent(AbstractMinimaxAgent):
    """Calculates utility of a game state solely based on the type and number of all pieces present"""
    def evaluation_function(self,state):
        friendly_pieces = state.get_pieces(self.color)
        enemy_pieces = state.get_pieces(~self.color)
        return self.get_all_piece_values(friendly_pieces) - self.get_all_piece_values(enemy_pieces)
    def get_all_piece_values(self,pieces):
        piece_mapping = {Pawn:1,Knight:3,Bishop:3.5,Rook:5,Queen:9,King:0}
        #No need for king value when the minimax tree ends if checkmate is reached
        score = 0
        for piece in pieces:
            score += piece_mapping[piece.__class__]
        return score




