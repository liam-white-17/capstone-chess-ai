import argparse,sys
from game import game
"""Main class"""

parser = argparse.ArgumentParser(description="Play a game of chess with or without AI functionality")
parser.add_argument("--load_file", help="load a chess game from a file",nargs='?')

args = parser.parse_args(sys.argv[1:])
if args.load_file:
    print(f'Loading file at {args.load_file[0]}')
game.run(vars(args))

