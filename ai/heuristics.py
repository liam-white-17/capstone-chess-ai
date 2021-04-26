"""
For evaluation functions on board state
"""
import math

from chess_lib.chess_utils import *
from chess_lib.chess_piece import *
# based on widely accepted value of pieces in chess theory, see https://en.wikipedia.org/wiki/Chess_piece_relative_value#Standard_valuations
DEFAULT_PIECE_VALUE_MAPPING = {Pawn: 10, Knight: 30, Bishop: 30, Rook: 50, Queen: 90, King: 900}


def piece_value_evaluation(state, color, piece_values=DEFAULT_PIECE_VALUE_MAPPING):
    def get_all_piece_values(pieces, piece_value_map):
        return sum([piece_value_map[piece.__class__] for piece in pieces])

    friendly_pieces = state.get_pieces(color)
    enemy_pieces = state.get_pieces(~color)
    return get_all_piece_values(friendly_pieces, piece_values) - get_all_piece_values(enemy_pieces, piece_values)


# def piece_location_evaluation(state, color, location_values, piece_values=DEFAULT_PIECE_VALUE_MAPPING):
#     def get_piece_location_values(pieces, location_values):
#         score = 0
#         for piece in pieces:
#             row, col = piece.get_loc()
#             if piece.color != Color.WHITE:
#                 row = 7 - row
#             piece_class = piece.__class__
#             score += piece_values[piece_class]
#             if piece_class in location_values.keys():
#                 score += location_values[piece_class][row][col]
#         return score
#
#     return get_piece_location_values(state.get_pieces(color), location_values) - get_piece_location_values(
#         state.get_pieces(~color), location_values)

def piece_location_evaluation(state, color, location_values):
    def get_piece_location_values(pieces, location_values):
        score = 0
        for piece in pieces:
            row, col = piece.get_loc()
            if piece.color != Color.WHITE:
                row = 7 - row
            piece_class = piece.__class__
            if piece_class in location_values.keys():
                score += location_values[piece_class][row][col]
        return score

    return get_piece_location_values(state.get_pieces(color), location_values) - get_piece_location_values(
        state.get_pieces(~color), location_values)

def best_heuristic(state,color):
    pass

DEFAULT_LOCATION_VALUES = {  # these values used as 'default'

Pawn: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.5, 0.25, 0, -2, -2, 0, 0.25, 0.5],
        [0.25, 0, 0.25, -0.5, -0.5, 0.25, 0, 0.25],
        [0, 0.25, 0.25, 1, 1, 0.5, 0.25, 0],
        [0.5, 1, 1.5, 2, 2, 1.5, 1, 0.5],
        [1, 2, 2.5, 3, 3, 2.5, 2, 1],
        [2, 2.5, 2.5, 3.5, 3.5, 2.5, 2.5, 2],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    King: [
        [0, 0, -0.5, -1, -1, -0.5, 0, 0],
        [0, 0, -1, -1.5, -1.5, -0.5, 0, 0],
        [-0.5, -1, -1.5, -2, -2, -1.5, -1, -0.5],
        [-1, -2, -2.5, -3, -3, -2.5, -2, -1],
        [-1, -2, -2.5, -3, -3, -2.5, -2, -1],
        [-1, -1.5, -1.5, -2, -2, -1.5, -1.5, -1],
        [-1, -1, -1.5, -1.5, -1.5, -1.5, -1.5, -1],
        [-0.5, -1, -1, -1, -1, -1, -1, -0.5]
    ],
    Queen: [
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
        [0, 0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0],
        [0.5, 0.5, 0.75, 1, 1, 0.75, 0.5, 0.5, ],
        [0.5, 0.75, 1, 2, 2, 1, 0.75, 0.5, ],
        [0.5, 0.75, 1, 2, 2, 1, 0.75, 0.5, ],
        [0.5, 0.5, 0.75, 1, 1, 0.75, 0.5, 0.5, ],
        [0, 0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0],
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0]
    ],
    Bishop: [
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0],
        [0, 0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0],
        [0.5, 0.5, 0.75, 1, 1, 0.75, 0.5, 0.5, ],
        [0.5, 0.75, 1, 2, 2, 1, 0.75, 0.5, ],
        [0.5, 0.75, 1, 2, 2, 1, 0.75, 0.5, ],
        [0.5, 0.5, 0.75, 1, 1, 0.75, 0.5, 0.5, ],
        [0, 0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0],
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, 0]
    ],
    Knight: [
        [-1, -0.75, 0, -0.5, -0.5, 0, -0.75, -1],
        [-1, -0.75, -0.5, 0, 0, -0.5, -0.75, -1],
        [0.5, 0.5, 1, 1.5, 1.5, 1, 0.5, 0.5, ],
        [0.75, 0.75, 1.5, 2, 2, 1.5, 0.5, 0.5, ],
        [0.75, 0.75, 1.5, 2.5, 2.5, 1.5, 0.5, 0.5, ],
        [0.5, 0.5, 0.75, 1, 1, 0.75, 0.5, 0.5, ],
        [0, 0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0],
        [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1]
    ],


}
# see https://www.chessprogramming.org/Simplified_Evaluation_Function
MICHNIEWSKI_PIECE_VALUES = {Pawn: 100, Knight: 320, Bishop: 350, Rook: 500, Queen: 900,
                            King: 900000}  # can't use math.inf for king as that would break utility calculation
MICHNIEWSKI_LOCATION_VALUES = {
    Pawn: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5, ],
        [5, -5, -10, 0, 0, -10, -5, 5, ],
        [0, 0, 0, 20, 20, 0, 0, 0, ],
        [5, 5, 10, 25, 25, 10, 5, 5, ],
        [10, 10, 20, 30, 30, 20, 10, 10, ],
        [50, 50, 50, 50, 50, 50, 50, 50, ],
        [0, 0, 0, 0, 0, 0, 0, 0, ]
    ],
    Knight: [
        [-50, -40, -30, -30, -30, -30, -40, -50, ],
        [-40, -20, 0, 5, 5, 0, -20, -40, ],
        [-30, 5, 10, 15, 15, 10, 5, -30, ],
        [-30, 0, 15, 20, 20, 15, 0, -30, ],
        [-30, 5, 15, 20, 20, 15, 5, -30, ],
        [-30, 0, 10, 15, 15, 10, 0, -30, ],
        [-40, -20, 0, 0, 0, 0, -20, -40, ],
        [-50, -40, -30, -30, -30, -30, -40, -50, ]
    ],
    Bishop: [
        [-20, -10, -10, -10, -10, -10, -10, -20, ],
        [-10, 5, 0, 0, 0, 0, 5, -10, ],
        [-10, 10, 10, 10, 10, 10, 10, -10, ],
        [-10, 0, 10, 10, 10, 10, 0, -10, ],
        [-10, 5, 5, 10, 10, 5, 5, -10, ],
        [-10, 0, 5, 10, 10, 5, 0, -10, ],
        [-10, 0, 0, 0, 0, 0, 0, -10, ],
        [-20, -10, -10, -10, -10, -10, -10, -20, ]
    ],
    Rook: [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5, ],
        [-5, 0, 0, 0, 0, 0, 0, -5, ],
        [-5, 0, 0, 0, 0, 0, 0, -5, ],
        [-5, 0, 0, 0, 0, 0, 0, -5, ],
        [-5, 0, 0, 0, 0, 0, 0, -5, ],
        [5, 10, 10, 10, 10, 10, 10, 5, ],
        [0, 0, 0, 0, 0, 0, 0, 0, ]
    ],
    Queen:[
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  5,  0,  0,  0,  0,-10,],
        [-10,  5,  5,  5,  5,  5,  0,-10,],
        [  0,  0,  5,  5,  5,  5,  0, -5,],
        [-5,  0,  5,  5,  5,  5,  0, -5,],
        [-10,  0,  5,  5,  5,  5,  0,-10,],
        [-10,  0,  0,  0,  0,  0,  0,-10,],
        [-20,-10,-10, -5, -5,-10,-10,-20,],
    ],
    King:[
        [20, 30, 10,  0,  0, 10, 30, 20],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [-10,-20,-20,-20,-20,-20,-20,-10,],
        [-20,-30,-30,-40,-40,-30,-30,-20,],
        [-30,-40,-40,-50,-50,-40,-40,-30,],
        [-30,-40,-40,-50,-50,-40,-40,-30,],
        [-30,-40,-40,-50,-50,-40,-40,-30,],
        [-30,-40,-40,-50,-50,-40,-40,-30,]
    ]
}
