## Introduction
This file contains explanations of how utility is calculated for LocationAgent, the 'best' AI, and why I implemented utility the way I did.

Because chess is a zero-sum game, the AI calculates utility by adding its own heuristic values and subtracting those of the opponent. For example, at the start of a game, the utility for both sides is zero. If white were to open with pe2e4, and the utility value for a pawn at e4 was 4, the white player would now have a utility value of 4 and black would have a utility of -4. 
## Piece values
The first and foremost heuristic the AI uses is the value of each piece on the board. The values I used here are widely accepted as an accurate assessment of chess piece's relative value (see [here](https://en.wikipedia.org/wiki/Chess_piece_relative_value)). In the AI's heuristic table, they have been multiplied by 10 for reasons described below.

Pawn: 10, Knight: 30, Bishop: 30, Rook: 50, Queen: 90, King: 900

Although the king would normally be represented as infinite due to its importance, doing so would prevent utility calculation from working properly. Instead, I used an arbitrarily large number that is greater than any possible number of pieces or positions (though the AI still treats a move that results in checkmate as having infinite utility; it does so by returning this value if the board state is a checkmate at any point)

## Location values

The other heuristic used for this AI was the location of its pieces on the board. The values vary depending on the piece; however, there is no possible change in utility that can be greater than 10--the value for a pawn. This was done deliberately; I decided I want the AI to prioritize pieces over positioning to prevent something like sacrificing a piece solely to gain a higher utility value from its positioning--unless said positioning would guarantee an opportunity to capture another piece of greater value.

The rest of this readme lists the location tables (from white's perspective on the board--the rows are in reverse order for black) and why they were chosen.
### Pawn

For pawns, I decided I want the AI to begin moving up its center pawns as soon as possible, so the utility value increases the closer the position is to the center. 

Leaving pawns in d2/e2 (white) or d7/e7 (black) is heavily penalized, as controlling the center with your pawns is one of the fundamental aspects of chess opening. From there, I increased utility values the further a pawn advances on the board--this encourages the AI to move its pawns foward, controlling more of the map and developing its own pieces.

I assigned a minor utility bonus for unmoved pawns on the outermost columns--this is to encourage the AI to leave the pawns there to protect its king after castling. 

The range of values here is much wider than any other piece--this is deliberate; I wanted the AI to focus on developing its pawns in the opening stages of the game. By the time this is done, the more valuable pieces will start getting opportunities to capture, which will always be prioritized over positioning.


Location value table:

  0     0     0     0     0     0     0     0
 
  2    2.5   2.5   3.5   3.5   2.5   2.5    2
 
  1     2    2.5    3     3    2.5    2     1
 
 0.5    1    1.5    2     2    1.5    1    0.5
 
  0   0.25  0.25    1     1    0.5  0.25    0

0.25    0   0.25  -0.5  -0.5  0.25    0   0.25

 0.5  0.25    0    -2    -2     0   0.25   0.5

  0     0     0     0     0     0     0     0
  
### King

The philosophy for the King's location value table was straightfoward: get the AI to castle as soon as possible and heavily penalize moving the king towards the center unless absolutely necessary.
 
Although some chess programmers have separate location value tables for the king in the 'endgame', I opted not to do this as defining the 'endgame' is subjective, and the AI is perfectly capable of winning by leaving its king well-defended even as pieces are captured.

Location value table:
-0.5   -1    -1    -1    -1    -1    -1   -0.5

 -1    -1   -1.5  -1.5  -1.5  -1.5  -1.5   -1

 -1   -1.5  -1.5   -2    -2   -1.5  -1.5   -1

 -1    -2   -2.5   -3    -3   -2.5   -2    -1

 -1    -2   -2.5   -3    -3   -2.5   -2    -1

-0.5   -1   -1.5   -2    -2   -1.5   -1   -0.5

  0     0    -1   -1.5  -1.5  -0.5    0     0

  0     0   -0.5   -1    -1   -0.5    0     0
  
 
### Knight
When first running the AI with my initial values for the knight (which were almost identical to the table for queen/bishop) I ran into some very poor opening techniques from the AI. It would almost never move its knights, opting instead to advance only its pawns, and would often move its knights to positions that really didn't provide any benefit strategically. 

Because of this, I modified the knight's location value table to penalize it for leaving knights in the corner. I also encourage it to control the center of the board. The range of values I used here is wider than those for the bishop/queen; this is deliberate, as while Queens and Bishops can theoretically move across the entire board, knights are quite slow. As such, the values I used encourage the AI to play aggressively with its knights and push forward in an effort to get in position to fork--which, in my opinion, is by far the most important use of knights in chess.

Location table:
 -1     0    0.5   0.5   0.5   0.5    0    -1
  0    0.5   0.5  0.75  0.75   0.5   0.5    0
 0.5   0.5  0.75    1     1   0.75   0.5   0.5
0.75  0.75   1.5   2.5   2.5   1.5   0.5   0.5
0.75  0.75   1.5    2     2    1.5   0.5   0.5
 0.5   0.5    1    1.5   1.5    1    0.5   0.5
 -1   -0.75 -0.5    0     0   -0.5  -0.75  -1
 -1   -0.75   0   -0.5  -0.5    0   -0.75  -1
 
### Queen/Bishop

I decided to use identical location tables for the queen and bishop as my goals for both pieces were the same. I wanted the AI to use its queen and bishops to control the center of the board and be able to reach as many tiles as possible.

That being said, the range of possible values for queens and bishops is lower than those of the knight and pawn tables; as bishops and queens can move quite far in a single turn, I wanted the AI to weigh their position a little less and focus on using these pieces to capture--saving the center for Knights and Pawns unless that's not a possibility.

Unlike the knight, there is no difference between the AI's corner and the opponent's in these tables. Again, Bishops and Queens can travel quite far, so it's not the end of the world if they're still in their starting corner--assuming the AI develops its pawns, which it is programmed to do.
 0     0    0.5   0.5   0.5   0.5    0     0
  0    0.5   0.5  0.75  0.75   0.5   0.5    0
 0.5   0.5  0.75    1     1   0.75   0.5   0.5
 0.5  0.75    1     2     2     1   0.75   0.5
 0.5  0.75    1     2     2     1   0.75   0.5
 0.5   0.5  0.75    1     1   0.75   0.5   0.5
  0    0.5   0.5  0.75  0.75   0.5   0.5    0
  0     0    0.5   0.5   0.5   0.5    0     0
  
### Rook

I deliberately did not include location tables for the Rook. There are a number of reasons for this--the primary one being that I wanted the AI to use its rooks defensively and keep them on their starting row. The AI is programmed to castle as soon as possible, and after this is done, the rooks will be connected--locking down the rearmost row and creating a great defensive position.

Rooks are also a very valuable piece, especially when both are present together. Leaving them in a defensive position encourages the AI to have both rooks in the later stages of the game--at which point, the AI's preference for capturing will outweigh positional tables.

This is not to say the AI will never move its rooks. In the later parts of the game, the AI begins using its rooks to capture pieces and put the opposing king in check--but the AI's focus on pieces over positions encourages this, so a location table is not necessary.

## Alternative methods of utility calculation (and why I didn't use them)
### Other piece-square tables
Although I initially intended to replace my own piece value tables with those of more experienced chess programmers, I decided not to for a number of reasons. The primary one was that in many cases, academic research into the 'best' piece-square tables is unavailable to the general public, so there were limited optoins online for me to attempt to replicate. 

However, I did implement the piece-value tables present in [Tomasz Michniewski's simplified evaluation function](https://www.chessprogramming.org/Simplified_Evaluation_Function), but found that when playing my own utility function against Michniewski's, the game would result in a stalemate. Furthermore, while my own implementation was able to beat the lesser PieceValueAgent, using Michniewski's AI would fail to do so, resulting in stalemate.
 
After some research, it seems that so long as the piece-square tables are in accordance with chess fundamentals, tweaking the exact numbers within has very little impact on the optimality of the AI using them. For all of these reasons, I decided to use my own implementation as the 'primary' AI, although Michniewski's evaluation function is still present in MichniewskiAgent for posterity.

### Other heuristics
There are a wide variety of options available to use in utility calculation beyond the location of pieces on the board--to name a few, attempting to check, prioritizing moves that allow the AI to make more moves, using chess openers, and many others.

When playing chess, the pieces available and their locations on the board are by far the most important considerations in evaluating ones own position. While putting an opponent in check CAN be helpful, this is not a guarantee, and I didn't want the AI to prioritize putting the opponent in check in the short term at the expense of the long-term advantage gained by one's own positioning. Many of the 'side effects' that check brings to the table--forking, forcing the opponent's king into bad positioning, etc--are prioritzed as an effect of minimax, so putting the opponent in check for the sake of it doesn't add anything to the table.

Similarly, prioritizing the number of moves available to the AI is an unintended consequence of the minimax algorithm--the piece-square tables are written to force the AI to put its pieces in areas where they will have the most possible moves on the board (i.e. the center). Prioritizing the number of moves available, in addition to being largely redundant, will also further increase the already significant compute times.

Although pre-programming common chess openings is also a sound idea in theory, in practice it is cumbersome and unnecessary. Admittedly, the AI does not play openings that match those of high-level chess grandmasters, but against the expected audience of the AI, this is a non-issue as the AI is perfectly capable of beating its expected audience even with unconventional openings. 

Furthermore, programming common openings requires very specific moves to be programmed in. The amount of openings that could be required for this to have any noticeable effect on the AI's planning is significant, and in addition to being computationally demanding, is difficult to program. There is also much debate about what the 'best' opening moves are--entire books have been written on a single opening move like pawn to e4. As such, the 'optimal' response for an AI to any given opening is extremely subjective.  