# Capstone-chess-ai
## Introduction
This is a chess game with functionality for playing with any combination of human and/or AI players for white or black.

All components were built using python3. Some external libraries were used for UI purposes, but all critical components were built by hand.
##Table of Contents:
* Requirements
* Installation
* Quickstart
## Requirements
* Python3.9
* [pip](https://pypi.org/project/pip/)
* [pypy](https://www.pypy.org/) (Optional, but HIGHLY recommended to reduce computation time) 

## Installation 
Before the project can be launched, external libraries must first be installed. This can be done by navigating to the directory from the terminal, and running
```pip install -r requirements.txt```

### Quickstart
If you just want to play against the AI and aren't interested in the additional options, run
```
pypy3 chess_ai.py -b --no-unicode
```


This will put you in a game against the 'best' AI available. The AI plays as black; to switch sides and have the AI play as white, replace '-b' with '-w'. 

**It is _strongly_ recommended that you use [pypy](https://www.pypy.org/) to run the AI as using the default python interpreter will result in significantly longer waits for the AI to make a move.**
To watch a game played between two AI's, run ```pypy3 chess_ai.py -b -w```

When first booting up the game, the command line will display a board like the following:
```

         a b c d e f g h

8        r h b q k b h r
7        p p p p p p p p
6        * * * * * * * *
5        * * * * * * * *
4        * * * * * * * *
3        * * * * * * * *
2        P P P P P P P P
1        R H B Q K B H R
```
White pieces are displayed by a capital letter, while black is displayed in lowercase. To avoid duplicating the K for King, knights are represented with an H for horse.
To make a move on the board, type the character of the piece to move followed by its original rank/file then its new rank/file.
For example, to move a pawn to e4, run
```
pe2e4
``` 
The board will then look like this:
```

         a b c d e f g h

8        r h b q k b h r
7        p p p p p p p p
6        * * * * * * * *
5        * * * * * * * *
4        * * * * P * * *
3        * * * * * * * *
2        P P P P * P P P
1        R H B Q K B H R
```
To make determining the input for a move easier, one can run '-m' in the command line for a list of all properly formatted valid moves.


To run the game with two optimal AIs, run with the following commands:
```
python chess_ai.py --white-agent LocationAgent --black-agent LocationAgent
```
To run with only one AI, omit the 'agent' command of your choosing.

Currently, the list of AI agents to chose from includes:
* RandomAgent: picks a random legal move. Intended as a baseline, obviously pretty easy to beat.
* FixedRandomAgent: same as RandomAgent except the seed for random.choice() is fixed constant, so FixedRandomAgent will always make the same move in a given board state. Used to compare the decision making of different AIs in a controlled environment.
* PieceValueAgent: chooses the move that will result in the maximum utility based on the value of each piece on the board. This agent picks the move that will maximize its own piece values while minimizing that of the opponent (though if it has the opportunity to checkmate, it'll just do that instead). 
* LocationAgent: The 'best' agent, and likely the one you want to use. Works like PieceValueAgent, except it also weighs the position of pieces on the board in its utility calculation.


## Project structure:
###Packages:
* `chess` -- contains classes and methods related to the rules of chess.
* `game` -- contains wrappers for the player to view/interact with the actual chess game.
* `ai` -- contains all AI agent classes.
* `test` -- contains unit tests and unit test input files. 
