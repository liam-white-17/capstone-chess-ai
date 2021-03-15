# Capstone-chess-ai
## Introduction
This is a chess game with functionality for playing with any combination of human and/or AI players for white or black.

All components were built using python3. Apart from those built in to python, no external libraries were used as of 3/14/21.

At this time, the only available AI agent is the 'RandomAgent'. As its name implies, the RandomAgent does not behave intelligently and randomly selects a legal move for its color. While the RandomAgent moves out of check, it does not assign any special weight to moves that capture pieces or win the game, making it quite easy for even an unskilled player to beat.

Upon completion, the AI should make use of the minimax algorithm to make intelligent moves in an effort to win games.

## Usage
Launching a game is straightforward. For a two person human game, simply run as follows:
```
python chess.py
```
The command line will then display a board like the following:
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


To run the game with two random AIs, run with the following commands:
```
python chess.py --white-agent RandomAgent --black-agent RandomAgent
```
To run with only one AI, omit the 'agent' command of your choosing.

## Project structure:
###Packages:
* `chess` -- contains classes and methods related to the rules of chess.
* `game` -- contains wrappers for the player to view/interact with the actual chess game.
* `ai` -- contains all AI agent classes.
* `test` -- contains unit tests and unit test input files. 
