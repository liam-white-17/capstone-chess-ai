import random
import time, logging
from abc import abstractmethod
from chess_lib.chess_utils import *
from chess_lib.chess_piece import *

from ai.agent import Agent
import math




class AbstractMinimaxAgent(Agent):
    """Abstract minimax agent that all minimax agents use as a superclass"""
    DEFAULT_MAX_DEPTH = 4  # depth increases each time min value is called from within max value or vice versa

    STALEMATE_VAL = -1 # could be set to zero but we want to avoid stalemates when all moves are equal
    WIN_VAL = math.inf
    LOSE_VAL = -math.inf

    def __init__(self, **args):
        Agent.__init__(self, **args)
        self.max_depth = args['depth'] if 'depth' in args else self.DEFAULT_MAX_DEPTH
        self.evaluation_function = None
        if 'logfile' in args:
            logging.basicConfig(filename=args['logfile'],level=logging.DEBUG,filemode='a')
        # else:
        #     logging.basicConfig(level=logging.DEBUG,filemode='a')



    def get_next_move(self, board):
        start = time.time()
        self.node_count = 0
        alpha0 = -math.inf
        beta0 = math.inf
        alpha = alpha0
        beta = beta0
        value = -math.inf
        best_move = None
        moves = []
        for piece in board.get_pieces(self.color):
            moves.extend([move for move in piece.get_valid_moves(board)])
        i=1
        # moves = []
        # for piece in board.get_pieces(self.color):
        #     piece_moves = piece.get_valid_moves(board)
        #     for poss_move in piece_moves:
        #         moves.append(poss_move)
        for curr_move in moves:
            successor = board.create_successor_board(curr_move)
            if is_check(successor,self.color):
                continue
            score = self.min_value(successor, curr_depth=1, alpha=alpha, beta=beta)
            if score > value:
                value = score
                best_move = curr_move
            if value >= beta:
                stop = time.time()
                delta = stop - start
                logging.debug(f'Score: {value:2f} time to find:{delta:2f} move: {best_move} Color: {self.color} Nodes searched: {self.node_count}')
                return best_move
            alpha = max(alpha, value)
        stop = time.time()
        delta = stop - start
        logging.debug(f'Score: {value:4f} Time to find move: {delta:2f} move: {best_move} Color: {self.color} Nodes searched: {self.node_count}')
        if best_move is None: #if we're not in stalemate (which is evaluated before calling the agent) and no move is 'good'
            # then the enemy is guaranteed a checkmate no matter what, so just pick a random legal move
            legal_moves = [move for move in moves if not is_check(board.create_successor_board(move),self.color)]
            return random.choice(legal_moves)
        return best_move

    def min_value(self, state, curr_depth, alpha, beta):
        # print(f'Depth = {curr_depth}')
        self.node_count += 1
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
        moves = []
        for piece in state.get_pieces(~self.color):
            moves.extend([move for move in piece.get_valid_moves(state)])
        # moves = []
        # for piece in state.get_pieces(~self.color):
        #     piece_moves = piece.get_valid_moves(state)
        #     for poss_move in piece_moves:
        #         moves.append(poss_move)
        for move in moves:
            successor = state.create_successor_board(move)
            if is_check(successor,~self.color):
                continue
            score = self.max_value(successor, curr_depth + 1, alpha, beta)
            val = min(val, score)
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val

    def max_value(self, state, curr_depth, alpha, beta):
        self.node_count += 1
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
        moves = []
        for piece in state.get_pieces(self.color):
            moves.extend([move for move in piece.get_valid_moves(state)])
        # moves = []
        # for piece in state.get_pieces(self.color):
        #     piece_moves = piece.get_valid_moves(state)
        #     for poss_move in piece_moves:
        #         moves.append(poss_move)
        for move in moves:
            successor = state.create_successor_board(move)
            if is_check(successor,self.color):
                continue
            score = self.min_value(successor, curr_depth + 1, alpha, beta)
            val = max(val, score)
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val

    def is_win(self, board):
        return is_checkmate(board,~self.color)
        # pieces = board.get_pieces(~self.color)
        # return not any([isinstance(piece, King) for piece in pieces])

    def is_lose(self, board):
        return is_checkmate(board,self.color)
        # pieces = board.get_pieces(self.color)
        # return not any([isinstance(piece, King) for piece in pieces])

    def is_tie(self, board):
        return is_stalemate(board,self.color)





class PieceValueAgent(AbstractMinimaxAgent):
    """Calculates utility of a game state solely based on the type and number of all pieces present"""

    def __init__(self, **args):
        AbstractMinimaxAgent.__init__(self, **args)
        self.evaluation_function = piece_value_evaluation

class WorsePieceValueAgent(PieceValueAgent):
    def __init__(self,**args):
        PieceValueAgent.__init__(self,**args)
        self.max_depth -= 1
class PieceLocationAgent(AbstractMinimaxAgent):
    def __init__(self,**args):
        AbstractMinimaxAgent.__init__(self,**args)
        self.evaluation_function = piece_location_evaluation

def piece_value_evaluation(state, color):
    def get_all_piece_values(pieces):
        return sum([piece_mapping[piece.__class__] for piece in pieces])

    friendly_pieces = state.get_pieces(color)
    enemy_pieces = state.get_pieces(~color)
    return get_all_piece_values(friendly_pieces) - get_all_piece_values(enemy_pieces)


def piece_location_evaluation(state, color):

    def get_piece_location_values(pieces):
        score = 0
        for piece in pieces:
            row,col = piece.get_loc()
            if piece.color != Color.WHITE:
                row = -row
            piece_class = piece.__class__
            score += piece_mapping[piece_class]
            if piece_class in piece_location_mapping.keys():
                score += piece_location_mapping[piece_class][row][col]
        return score
    return get_piece_location_values(state.get_pieces(color)) - get_piece_location_values(state.get_pieces(~color))



piece_mapping = {Pawn: 10, Knight: 30, Bishop: 30, Rook: 50, Queen: 90, King: 900}
piece_location_mapping = {
    Pawn: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.1, 0.12, 0.13, 0.14, 0.14, 0.13, 0.12, 0.1],
        [0.2, 0.21, 0.22, 0.23, 0.23, 0.22, 0.21, 0.2],
        [0.3, 0.31, 0.32, 0.33, 0.33, 0.32, 0.31, 0.3],
        [0.44, 0.45, 0.46, 0.47, 0.47, 0.46, 0.45, 0.44],
        [0.51, 0.53, 0.55, 0.57, 0.57, 0.55, 0.53, 0.51],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
}
