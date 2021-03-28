from abc import abstractmethod
import time, logging
from chess_lib.chess_utils import *
from chess_lib.chess_piece import *

from ai.agent import Agent
import math

logging.basicConfig(level=logging.DEBUG)


class AbstractMinimaxAgent(Agent):
    """Abstract minimax agent that all minimax agents use as a superclass"""
    DEFAULT_MAX_DEPTH = 3  # depth increases each time min value is called from within max value or vice versa

    STALEMATE_VAL = 0
    WIN_VAL = math.inf
    LOSE_VAL = -math.inf

    def __init__(self, **args):
        Agent.__init__(self, **args)
        self.max_depth = args['depth'] if 'depth' in args else self.DEFAULT_MAX_DEPTH
        self.evaluation_function = None

    def get_next_move(self, board):

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
            score = self.min_value(successor, curr_depth=0, alpha=alpha, beta=beta)
            if score > value:
                value = score
                best_move = curr_move
            if value >= beta:
                stop = time.time()
                delta = stop - start
                logging.debug(f'Score: {value} time to find:{delta}')
                return best_move
            alpha = max(alpha, value)
        stop = time.time()
        delta = stop - start
        logging.debug(f'Score: {value} Time to find move: {delta} Agent type: A/B')
        return best_move

    def min_value(self, state, curr_depth, alpha, beta):
        # print(f'Depth = {curr_depth}')
        if self.is_win(state):
            return self.WIN_VAL
        if self.is_lose(state):
            return self.LOSE_VAL
        if self.is_tie(state):
            return self.STALEMATE_VAL
        if curr_depth == self.max_depth:
            score = self.evaluation_function(state, self.color)
            # print(f'Depth = {curr_depth} score = {score}')
            return score
        val = math.inf
        moves = state.get_all_moves(~self.color)
        for move in moves:
            successor = state.create_successor_board(move)
            score = self.max_value(successor, curr_depth + 1, alpha, beta)
            val = min(val, score)
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val

    def max_value(self, state, curr_depth, alpha, beta):
        if self.is_win(state):
            return self.WIN_VAL
        if self.is_lose(state):
            return self.LOSE_VAL
        if self.is_tie(state):
            return self.STALEMATE_VAL
        if curr_depth == self.max_depth:
            score = self.evaluation_function(state, self.color)
            # print(f'Depth = {curr_depth} score = {score}')
            return score
        val = -math.inf
        moves = state.get_all_moves(self.color)
        for move in moves:
            successor = state.create_successor_board(move)
            score = self.min_value(successor, curr_depth + 1, alpha, beta)
            val = max(val, score)
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val

    def is_win(self, board):
        # return is_checkmate(board,self.color)
        pieces = board.get_pieces(~self.color)
        return not any([isinstance(piece, King) for piece in pieces])

    def is_lose(self, board):
        pieces = board.get_pieces(self.color)
        return not any([isinstance(piece, King) for piece in pieces])

    def is_tie(self, board):
        return no_valid_moves(board, self.color) and not is_check(board, self.color)





class PieceValueAgent(AbstractMinimaxAgent):
    """Calculates utility of a game state solely based on the type and number of all pieces present"""

    def __init__(self, **args):
        AbstractMinimaxAgent.__init__(self, **args)
        self.evaluation_function = piece_value_evaluation


def piece_value_evaluation(state, color):
    def get_all_piece_values(pieces):
        piece_mapping = {Pawn: 10, Knight: 30, Bishop: 30, Rook: 50, Queen: 90, King: 900}
        # No need for king value when the minimax tree ends if checkmate is reached
        score = 0
        for piece in pieces:
            score += piece_mapping[piece.__class__]
        return score

    friendly_pieces = state.get_pieces(color)
    enemy_pieces = state.get_pieces(~color)
    return get_all_piece_values(friendly_pieces) - get_all_piece_values(enemy_pieces)


# def piece_location_evaluation(state, color):
#     pass
#
#
# piece_location_mapping = {
#     Pawn: [
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0.5, 1, 1.5, 1.5, 1, 0.5, 0],
#         [0, 1, 2, 3, 3, 2, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#     ]
# }
