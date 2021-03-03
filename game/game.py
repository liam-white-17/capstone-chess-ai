import sys
from game.player import Player
from chess.game_board import Board
from chess.chess_utils import Color, convert_int_to_rank_file as xy_to_rf, convert_rank_file_to_int as rf_to_xy, \
    is_check, is_checkmate, no_valid_moves
from chess.move import Move


class ChessGame:

    def __init__(self, **args):

        self.board = Board().new_game() if 'load_file' not in args or args['load_file'] is None \
            else Board.load_from_file(args['load_file'])
        # setting AI as None indicates that the color white/black is human controlled

        self.white_AI = None
        self.black_AI = None

        self.player_to_move = Color.WHITE

        self.no_graphics = True  # TODO add command-line options to enable UI (once UI is completed)
        self.stdin = sys.stdin
        self.stdout = sys.stdout

    def run_game(self):
        game_over = False
        # TODO separate into UI vs command-line run-game types
        print('Launching new game of chess...')

        while not game_over:
            print('Current Board state:\n')
            print(self.board.display_board())
            if is_checkmate(self.board,self.player_to_move):
                print(f'{self.player_to_move} is in checkmate. {~self.player_to_move} wins!')
                game_over = True
                break
            elif no_valid_moves(self.board,self.player_to_move) and not is_check(self.board,self.player_to_move):
                print(f'{self.player_to_move} is in stalemate. Match is a draw!')
                game_over=True
                break
            elif is_check(self.board,self.player_to_move):
                print(f'{self.player_to_move} is in check!')
            print(f'It is {self.player_to_move} to move.')
            move = self.get_next_move()
            self.process_move(move)


    def get_next_move(self):
        valid_move_recieved = False
        while not valid_move_recieved:
            print()
            cli_input = input('Please enter the move you would like to make (for formatting options, type -h):\n')
            if cli_input == '-h':
                print("""Moves should be of the format <piece><original rank><original file><new rank><new file>.
                For instance, to move a white pawn from c2 to c4, you would type 'Pc2c4'.
                To move a black knight from g8 to capture a piece at f6, type 'Hg8xf6'.
                The 'x' for capturing is not required, but can be included. 
                """)
            elif cli_input in ['-e','exit','--exit']:
                sys.exit(0)
            else:
                try:
                    move = Move.create_move_from_str(self.board, cli_input, self.player_to_move)
                    return move
                except ValueError as e:
                    print(f'Invalid input recieved: {e}')

    def process_move(self, move):
        src = move.src
        dest = move.dest
        piece_to_move = self.board.piece_at(*src)
        if piece_to_move is None:
            print(f'Invalid input received: no piece located at {xy_to_rf(src)}')
            return
        if piece_to_move.get_color() != self.player_to_move:
            print(f'Invalid input received: wrong color of piece at {xy_to_rf(src)}')
        valid_moves = piece_to_move.get_valid_moves(self.board, src)
        if move not in valid_moves:
            print(f'Invalid input received: piece at {xy_to_rf(src)} cannot legally move to {xy_to_rf(dest)}')
            return
        successor = self.board.create_successor_board(move)
        if is_check(successor, self.player_to_move):
            print(f'Invalid input received: move from {xy_to_rf(src)} to {xy_to_rf(dest)} ' +
                  f'would put {self.get_player_to_move(as_string=True)} in check.')
            return
        self.board = successor
        self.player_to_move = ~self.player_to_move


    def get_player_to_move(self, as_string=False):
        if as_string:
            return 'white' if self.player_to_move else 'black'
        else:
            return self.player_to_move


def run(args):
    curr_game = ChessGame(**args)
    curr_game.run_game()