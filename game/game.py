# -*- coding: utf-8 -*-
import codecs
import sys, time
from chess_lib import chess_piece
from chess_lib.game_board import Board
from chess_lib.chess_utils import Color, convert_int_to_rank_file as xy_to_rf, convert_rank_file_to_int as rf_to_xy, \
    is_check, is_checkmate, no_valid_moves
from ai.agent import *
from ai.minimax_agent import *



class ChessGame:
    """The UI wrapper through which the user engages in a game of chess."""
    def __init__(self, **args):
        # print(sys.stdout.encoding)
        # sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.buffer.detach())
        # print(sys.stdout)
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
        self.board = Board().new_game() if 'load_file' not in args or args['load_file'] is None \
            else Board.load_from_file(args['load_file'])
        # setting AI as None indicates that the color white/black is human controlled

        self.white_AI = None
        self.black_AI = None
        self.winner = None

        self.UNDO_VALUE = 'undo'
        if args['use-white-ai']:
            white_ai_type = PieceLocationAgent if args['white-agent'] is None else \
                get_agent_from_string(args['white-agent'],Color.WHITE)
            self.white_AI = white_ai_type(color=Color.WHITE,**args)
        if args['use-black-ai']:
            black_ai_type = PieceLocationAgent if args['black-agent'] is None else \
                get_agent_from_string(args['black-agent'], Color.BLACK)
            self.black_AI = black_ai_type(color=Color.BLACK, **args)


        self.player_to_move = Color.WHITE

        self.no_graphics = True

        self.turn_num = 1
        self.recent_board_states = []
        self.max_states_kept = 20
        self.max_repetition = 5
        self.fifty_move_rule_counter = 0  # under FIDE rules, a game is a draw when no player has moved a pawn or captured a piece
        # in the past 50 turns
        self.use_unicode = not (args['no-unicode'])
        if self.use_unicode:
            self.test_unicode() #checks to see if unicode is possible


    def run_game(self):

        print('Launching new game of chess...')

        while 1:
            print(f'Beginning turn {self.turn_num} for {self.get_player_to_move(as_string=True)}')

            print('Current Board state:\n')
            try:
                self.board.display_board(unicode=self.use_unicode)
            except:
                self.use_unicode = False
                self.board.display_board(unicode=self.use_unicode)
            if is_checkmate(self.board, self.player_to_move):
                print(f'{self.player_to_move} is in checkmate. {~self.player_to_move} wins!')
                self.winner = ~self.player_to_move
                break
            elif is_stalemate(self.board, self.player_to_move):
                print(
                    f'{self.player_to_move} is either in stalemate or it is no longer possible for either player to win.' + \
                    ' Match is a draw!')
                break
            elif self.is_threefold_repetition():
                print('Match is a draw due to "threefold repetition", where the same board is repeated three times.')
                break
            elif self.fifty_move_rule_counter >= 50:
                print('Match is a draw due to fifty moves without any capturing or pawn movement by either side')
                break
            elif is_check(self.board, self.player_to_move):
                print(f'{self.player_to_move} is in check!')
            print(f'It is {self.player_to_move} to move.')
            move = self.get_next_move()
            if move is None:
                continue
            else:
                self.process_move(move)
        if not isinstance(self,Analysis):
            response = input('Play again? (y/n):')
            if response in ['y','Y','yes']:
                self.board = Board().new_game()
                self.winner = None
                self.player_to_move = Color.WHITE
                self.turn_num = 1
                self.recent_board_states = []
                self.fifty_move_rule_counter = 0
                self.run_game()
            else:
                print('Thanks for playing!')
                sys.exit(0)

    def get_next_move(self):
        #print(self.black_AI.evaluation_function(self.board, Color.BLACK))
        if self.player_to_move == Color.WHITE and self.white_AI is not None:
            print('Calculating, this may take a while...')
            return self.white_AI.get_next_move(self.board)
        if self.player_to_move == Color.BLACK and self.black_AI is not None:
            print('Calculating, this may take a while...')
            return self.black_AI.get_next_move(self.board)

        valid_move_recieved = False
        while not valid_move_recieved:
            print()

            cli_input = input(
                "Please enter the move you would like to make.\nFor formatting requirements and additional commands, type -h" +
                "\n\n""")
            if cli_input == '-h':
                print("""Moves should be of the format <piece><original rank><original file><new rank><new file>.
                For instance, to move a white pawn from c2 to c4, you would type 'Pc2c4'.
                To move a black knight from g8 to capture a piece at f6, type 'Hg8xf6'.
                The 'x' for capturing is not required, but can be included.
                If the move would move a pawn to the end of the board, append an equals sign followed by the piece""" + \
                      """you would like to promote the pawn to (e.x. Pc7c8=Q)
                      Castling is denoted by 0-0 (kingside) or 0-0-0 (queenside).
                      Additional commands:
                      -m,--moves : lists all legal moves at this board state, with proper formatting.
                      -u,--undo  : undo the previous two moves, reverting the board back to previous state. 
                                   Note that due to memory constraints, a limited number of consecutive undos can be performed.
                      -p,--pieces: lists material (pieces) available to current player.
                      -e,--exit  : exits the program
                      """)
            elif cli_input in ['-m', '--moves']:
                for valid_move in self.board.get_all_moves(self.player_to_move):
                    print(valid_move, end=', ')
            elif cli_input in ['-p','--pieces','-P']:
                self.print_material()
            elif cli_input in ['-e', 'exit', '--exit']:
                sys.exit(0)
            elif cli_input in ['-u', '--undo', 'undo']:
                length = len(self.recent_board_states)
                if length == 0:
                    print('Maximum number of undos reached.')
                else:
                    if length == 1:
                        self.player_to_move = ~self.player_to_move
                        self.board = self.recent_board_states[-1]
                        self.recent_board_states.pop()
                    else:
                        self.turn_num -= 1
                        self.fifty_move_rule_counter -= 2
                        self.recent_board_states.pop()
                        self.board = self.recent_board_states[-1]
                        self.recent_board_states.pop()
                    return None
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
            print(f'Invalid input received: piece at {xy_to_rf(src)} cannot legally move to {xy_to_rf(dest)},' + \
                  'or you aren\'t specifying the piece type in a pawn promotion.')
            return
        successor = self.board.create_successor_board(move)
        if is_check(successor, self.player_to_move):
            print(f'Invalid input received: move from {xy_to_rf(src)} to {xy_to_rf(dest)} ' +
                  f'would put {self.get_player_to_move(as_string=True)} in check.')
            return
        if isinstance(successor.piece_at(*move.dest), chess_piece.Pawn) and move.dest[0] in (0, 8):
            print(f'Invalid input recieved: pawn in illegal location after move processed.')
            print('If this move puts a pawn at the end of the board, make sure you specify the promotion type')
            return
        if len(self.recent_board_states) > self.max_states_kept:
            self.recent_board_states.pop(0)
        self.recent_board_states.append(self.board.__deepcopy__())
        self.board = successor
        self.player_to_move = ~self.player_to_move
        if self.player_to_move == Color.WHITE:
            self.turn_num += 1
        if isinstance(piece_to_move, Pawn) or move.piece_captured is not None:
            self.fifty_move_rule_counter = 0
        else:
            self.fifty_move_rule_counter += 1

    def print_material(self, print_positions=True):
        class_to_name_map = {Pawn:'Pawn',Knight:'Knight',Bishop:'Bishop',Rook:'Rook',Queen:'Queen',King:'King'}
        white_pieces = self.board.get_pieces(Color.WHITE)
        black_pieces = self.board.get_pieces(Color.BLACK)
        print('WHITE:')
        for white_piece in white_pieces:
            if print_positions:
                print(f'{class_to_name_map[white_piece.__class__]} at {convert_int_to_rank_file(white_piece.get_loc())}')
            else:
                print(f'{class_to_name_map[white_piece.__class__]}')
        print('BLACK:')
        for black_piece in black_pieces:
            if print_positions:
                print(f'{class_to_name_map[black_piece.__class__]} at {convert_int_to_rank_file(black_piece.get_loc())}')
            else:
                print(f'{class_to_name_map[black_piece.__class__]}')



    def is_threefold_repetition(self):
        if len(self.recent_board_states) <= self.max_states_kept:
            return False
        for state in self.recent_board_states:
            if self.recent_board_states.count(state) >= self.max_repetition:
                return True
        return False

    def get_player_to_move(self, as_string=False):
        if as_string:
            return 'white' if self.player_to_move else 'black'
        else:
            return self.player_to_move
    def test_unicode(self):
        try:
            chars = "♔♕♖♗♘♙"
            expected = "♔♕♖♗♘♙"
            actual = chars.encode(sys.stdout.encoding).decode('utf-8')
            self.use_unicode = expected == actual
            #self.use_unicode =  expected == actual
        except Exception as e:
            print(f'Exception generated from attempting to use unicode: {e}. Using ASCII characters instead...')
            self.use_unicode = False


def get_agent_from_string(agent_name,color):
    color_string = 'white' if color else 'black'
    agents = {'RandomAgent': RandomAgent, 'PieceValueAgent': PieceValueAgent,
              'FixedRandomAgent': FixedRandomAgent, 'LocationAgent': PieceLocationAgent,
              'MichniewskiAgent': MichniewskiAgent}
    try:

        return agents[agent_name]
    except KeyError as e:
        print(f'ERROR: invalid AI agent specified for {color_string}. List of accepted agents:', end=' ')
        for key in agents.keys():
            print(key, end=' ')
        print(f'\nUsing default AI for {color_string} instead.')
        return PieceLocationAgent


class Analysis(ChessGame):
    """Used for analysis by the author, please ignore this code."""

    def __init__(self, **args):

        self.time_per_move = []
        self.board_states = []
        self.OUT_DIR = 'analysis'
        curr_time = time.gmtime()
        timestamp = '-'.join([str(i) for i in curr_time[1:3]]) + '_' + '-'.join([str(i) for i in curr_time[3:6]])
        if args['outfile'] is None:
            self.basefile_name = f'{self.OUT_DIR}/{timestamp}-{args["white-agent"]}-{args["black-agent"]}'
        else:
            self.basefile_name = f'{timestamp}-{args["outfile"]}'
        self.outfile_name = self.OUT_DIR + '/' + self.basefile_name + '.txt'
        print(f'Output sent to {self.outfile_name}')

        self.agent_to_track = Color.WHITE if args[
            'track_white'] else Color.BLACK
        args['logfile'] = self.OUT_DIR + '/' + self.basefile_name + '_LOG.txt'
        print(f'Logs found at {args["logfile"]}')
        orig_stdout = sys.stdout
        sys.stdout = open(self.outfile_name, 'a')
        ChessGame.__init__(self, **args)

    def run_game(self):
        ChessGame.run_game(self)
        avg = sum(self.time_per_move) / len(self.time_per_move)
        mintime = min(self.time_per_move)
        maxtime = max(self.time_per_move)
        if self.winner is None:
            print(f'SUMMARY: stalemate reached in {self.turn_num} moves,' + \
                  f'with an average time per move of {avg}, a min time of {mintime} and max time of {maxtime}')
        else:
            print(f'SUMMARY: {self.winner} beat {~self.winner} in {self.turn_num} moves, ' + \
                  f'with an average time per move of {avg}, a min time of {mintime} and a max time of {maxtime}')

    def get_next_move(self):
        start = time.time()
        move = ChessGame.get_next_move(self)
        stop = time.time()
        delta = stop - start
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
