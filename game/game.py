import sys, time
from util import Stack
from chess_lib import chess_piece
from chess_lib.game_board import Board
from chess_lib.chess_utils import Color, convert_int_to_rank_file as xy_to_rf, convert_rank_file_to_int as rf_to_xy, \
    is_check, is_checkmate, no_valid_moves
from chess_lib.move import Move
from ai.agent import *
from ai.minimax_agent import *
from os import getcwd


class ChessGame:

    def __init__(self, **args):

        self.board = Board().new_game() if 'load_file' not in args or args['load_file'] is None \
            else Board.load_from_file(args['load_file'])
        # setting AI as None indicates that the color white/black is human controlled

        self.white_AI = None
        self.black_AI = None
        self.winner = None
        if args['white-agent'] is not None:
            self.white_AI = get_agent_from_string(args['white-agent'])(color=Color.WHITE)
        if args['black-agent'] is not None:
            self.black_AI = get_agent_from_string(args['black-agent'])(color=Color.BLACK)

        self.player_to_move = Color.WHITE

        self.no_graphics = True  # TODO add command-line options to enable UI (once UI is completed)

        self.turn_num = 1
        self.move_history = Stack()



    def run_game(self):
        game_over = False
        # TODO separate into UI vs command-line run-game types
        print('Launching new game of chess_lib...')

        while not game_over:
            print(f'Beginning turn {self.turn_num} for {self.get_player_to_move(as_string=True)}')
            # if self.turn_num % 10 == 0:
            #     time.sleep(1.0)
            print('Current Board state:\n')
            print(self.board.display_board())
            if is_checkmate(self.board,self.player_to_move):
                print(f'{self.player_to_move} is in checkmate. {~self.player_to_move} wins!')
                self.winner = ~self.player_to_move
                game_over = True
                break
            elif no_valid_moves(self.board,self.player_to_move) and not is_check(self.board,self.player_to_move):
                print(f'{self.player_to_move} is either in stalemate or it is no longer possible for either player to win.'+\
                      ' Match is a draw!')
                game_over=True
                break
            elif is_check(self.board,self.player_to_move):
                print(f'{self.player_to_move} is in check!')
            print(f'It is {self.player_to_move} to move.')
            move = self.get_next_move()
            self.process_move(move)


    def get_next_move(self):
        if self.player_to_move == Color.WHITE and self.white_AI is not None:
            return self.white_AI.get_next_move(self.board)
        if self.player_to_move == Color.BLACK and self.black_AI is not None:
            return self.black_AI.get_next_move(self.board)


        valid_move_recieved = False
        while not valid_move_recieved:
            print()

            cli_input = input("Please enter the move you would like to make.\nFor formatting options, type -h"+
            "\nTo see a list of all valid moves, type -m\n""")
            if cli_input == '-h':
                print("""Moves should be of the format <piece><original rank><original file><new rank><new file>.
                For instance, to move a white pawn from c2 to c4, you would type 'Pc2c4'.
                To move a black knight from g8 to capture a piece at f6, type 'Hg8xf6'.
                The 'x' for capturing is not required, but can be included.
                If the move would move a pawn to the end of the board, append an equals sign followed by the piece"""+\
                """you would like to promote the pawn to (e.x. Pc7c8=Q)
                Castling is denoted by 0-0 (kingside) or 0-0-0 (queenside). 
                """)
            elif cli_input in ['-m','--moves']:
                for valid_move in self.board.get_all_moves(self.player_to_move):
                    print(valid_move,end=', ')
            elif cli_input in ['-e','exit','--exit']:
                sys.exit(0)
            else:
                try:
                    move = chess_piece.create_move_from_str(self.board, cli_input, self.player_to_move)
                    return move
                except ValueError as e:
                    print(f'Invalid input recieved: {e}')

    def process_move(self, move):
        if self.player_to_move == Color.WHITE and self.white_AI is not None:
            print(f'White move: {move}')
        if self.player_to_move == Color.BLACK and self.black_AI is not None:
            print(f'Black move: {move}')
        src = move.src
        dest = move.dest
        piece_to_move = self.board.piece_at(*src)
        if piece_to_move is None:
            print(f'Invalid input received: no piece located at {xy_to_rf(src)}')
            return
        if piece_to_move.get_color() != self.player_to_move:
            print(f'Invalid input received: wrong color of piece at {xy_to_rf(src)}')
            return
        valid_moves = piece_to_move.get_valid_moves(self.board, src)
        if move not in valid_moves:
            print(f'Invalid input received: piece at {xy_to_rf(src)} cannot legally move to {xy_to_rf(dest)},'+\
            'or you aren\'t specifying the piece type in a pawn promotion.')
            return
        successor = self.board.create_successor_board(move)
        if is_check(successor, self.player_to_move):
            print(f'Invalid input received: move from {xy_to_rf(src)} to {xy_to_rf(dest)} ' +
                  f'would put {self.get_player_to_move(as_string=True)} in check.')
            return
        if isinstance(successor.piece_at(*move.dest),chess_piece.Pawn) and move.dest[0] in (0,8):
            print(f'Invalid input recieved: pawn in illegal location after move processed.')
            print('If this move puts a pawn at the end of the board, make sure you specify the promotion type')
            return
        self.board = successor
        self.player_to_move = ~self.player_to_move
        if self.player_to_move:
            self.turn_num += 1


    def get_player_to_move(self, as_string=False):
        if as_string:
            return 'white' if self.player_to_move else 'black'
        else:
            return self.player_to_move

def get_agent_from_string(agent_name):
    agents = {'RandomAgent': RandomAgent,'PieceValueAgent':PieceValueAgent,
              'FixedRandomAgent':FixedRandomAgent,'Multithread':MultithreadedMinimaxAgent}
    try:

        return agents[agent_name]
    except KeyError as e:
        print(f'ERROR: invalid AI agent specified. List of accepted agents:',end=' ')
        for key in agents.keys():
            print(key,end=' ')
        print('Exiting...')
        sys.exit(0)

class Analysis(ChessGame):
    """Used for analysis by the author, please ignore this code."""
    def __init__(self,**args):
        ChessGame.__init__(self,**args)
        self.time_per_move = []
        self.board_states=[]
        self.OUT_DIR = 'analysis'
        curr_time = time.gmtime()
        timestamp = '-'.join([str(i) for i in curr_time[1:3]])+'_'+'-'.join([str(i) for i in curr_time[3:6]])
        if args['outfile'] is None:
            self.outfile_name = f'{self.OUT_DIR}/{timestamp}-{args["white-agent"]}-{args["black-agent"]}.txt'
        else:
            self.outfile_name = f'{self.OUT_DIR}/{timestamp}-{args["outfile"]}.txt'
        print(f'Output sent to {self.outfile_name}')
        orig_stdout = sys.stdout
        sys.stdout = open(self.outfile_name,'w')
        self.agent_to_track = Color.BLACK #todo add option to specify tracking of white OR black
    def run_game(self):
        ChessGame.run_game(self)
        avg = sum(self.time_per_move)/len(self.time_per_move)
        mintime = min(self.time_per_move)
        maxtime = max(self.time_per_move)
        print(f'SUMMARY: {self.winner} beat {~self.winner} in {self.turn_num} moves, '+\
                f'with an average time per move of {avg}, a min time of {mintime} and a max time of {maxtime}')

    def get_next_move(self):
        start = time.time()
        move = ChessGame.get_next_move(self)
        stop = time.time()
        delta = stop-start
        if self.player_to_move == self.agent_to_track:
            self.time_per_move.append(delta)
            print(f'Time to move: {delta}')
        return move


def run(args):
    if args['do-analysis']:
        curr_game = Analysis(**args)
    else:
        curr_game = ChessGame(**args)
    curr_game.run_game()
