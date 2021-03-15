import argparse, sys
from game import game

"""Main class"""
usage_msg = """
USAGE:      python chess.py <options>
EXAMPLES:   (1) python chess.py
            - starts a new game with two human players
            (2) python chess.py -w RandomAgent 
            OR  python chess.py --white-agent RandomAgent
            - starts a new game with a human playing for black and a randomly acting AI playing for white
            (3) python chess.py -b RandomAgent
            OR python chess.py --black-agent RandomAgent
            - starts a new game as in (2) except white is played by human and black is played by AI
            (3) python chess.py --load_file path/to/file.txt 
            - loads a previously played chess game stored in a text file
             
"""
parser = argparse.ArgumentParser(description=usage_msg)
parser.add_argument("--load_file",
                    help="Load a chess game from a file. Please note that this feature is a WIP and games loaded from a file may not work correctly",
                    nargs='?')
parser.add_argument("-w", "--white-agent", help='AI agent used to represent white player', default=None,
                    dest='white-agent')
parser.add_argument("-b", "--black-agent", help='AI agent used to represent black player', default=None,
                    dest='black-agent')

args = parser.parse_args(sys.argv[1:])
if args.load_file:
    print(f'Loading file at {args.load_file[0]}')
game.run(vars(args))
