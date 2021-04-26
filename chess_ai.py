# -*- coding: utf-8 -*-
import argparse, sys
from game import game

"""Main class"""
usage_msg = """
USAGE:      python chess_ai.py <options>
EXAMPLES:   (1) python chess_ai.py
            - starts a new game with two human players
            (2) python chess_ai.py -w RandomAgent 
            OR  python chess_ai.py --white-agent RandomAgent
            - starts a new game with a human playing for black and a randomly acting AI playing for white
            (3) python chess_ai.py -b RandomAgent
            OR python chess_ai.py --black-agent RandomAgent
            - starts a new game as in (2) except white is played by human and black is played by AI
            (3) python chess_ai.py --load_file path/to/file.txt 
            - loads a previously played chess game stored in a text file
             
"""
parser = argparse.ArgumentParser(description=usage_msg)

parser.add_argument('-w','--white-ai',help="Specifies that the white player will be an AI",action='store_true',dest='use-white-ai')
parser.add_argument('-b','--black-ai',help="Specifies that the black player will be an AI",action='store_true',dest='use-black-ai')
parser.add_argument("-W", "--white-ai-type", help='AI agent used to represent white player. Optional; by default this will use the location agent, the most optimal AI. For a full list, see the readme.', default=None,
                    dest='white-agent')
parser.add_argument("-B", "--black-ai-type", help='AI agent used to represent black player, works as -w/--white-ai-type', default=None,
                    dest='black-agent')
parser.add_argument('-d','--depth',help='Maximum depth of the decision tree used in move generation. The default is 4; '
                    'however,you may find that using a lower depth can help speed up move generation if the speed is too low.'
                    'As lowering the depth significantly worsens strategic decision making, please attempt to run the '
                    'program using pypy3 for its speed benefits before reducing depth. For more information, consult the readme.',
                    action='store',type=int,default=4,dest='depth')
parser.add_argument('--no-unicode',
                    help='Specifying this option will replace unicode chess characters (the default) with letters '
                         'representing each piece.Note that unicode is not supported in all terminals (in which case '
                         'the program will automatically use letters).',
                    action='store_true', dest='no-unicode')
# these arguments used for analysis of AI speed/optimality. Should not come up in a normal presentation
parser.add_argument("--load-file",
                    help=argparse.SUPPRESS,
                    nargs='?')
parser.add_argument('-a', '--analysis', help=argparse.SUPPRESS,
                    action='store_true',
                    dest='do-analysis')
parser.add_argument('-T', '--track-white', help=argparse.SUPPRESS,
                    action='store_true',
                    dest='track_white')
parser.add_argument('-o', '--outfile', help=argparse.SUPPRESS, default=None,
                    dest='outfile')

args = parser.parse_args(sys.argv[1:])
if args.load_file:
    print(f'Loading file at {args.load_file[0]}')
game.run(vars(args))
