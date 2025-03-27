# PrinceDomino
PrinceDomino is a Python implementation of the 2016 board game Kingdomino. I started this project to practice coding in Python and using GitHub.


### Setup

You can play PrinceDomino in the terminal by cloning this repository and running **Play.py**. When you do, the script will prompt for startup information before beginning the game.

![The terminal asks startup questions, such as how many players there are and what scoring rules to use.](/images/setup.png)

### Playing the Game

On their turn, a player does two things. **First**, they place their current domino on the board. The following inputs are allowed during this step. (Inputs are not case sensitive)

- **Coordinate** - Specify the alphabetic column and the numeric row to place the current tile. E.g. "*A4*", "*3a*" or "*g7*". The game attempts to place the asterisk (*) part of the tile on the specified coordinate.
    - If the coordinate is invalid, a message will explain why the placement was invalid.
- **"R"** or **"r"** to rotate the tile.
- **"P"** or **"p"** to pass.
    - (This should only work if there are no valid moves)

![The terminal displays a 7x7 grid with multiple terrains. Beneath that is a list of tiles available for the next round, a message explaining an invalid move, and a prompt for the next move.](/images/playing.png)

Because a player can build in any direction, the player's board is recentered after each placement to keep it within the bounds of the grid.

**Second**, the player chooses which domino to place next round. The chosen domino determines the player order for the next round.

If the player made a mistake on their turn, they can type **"U"** or **"u"** to return to the start of the turn.

### Scoring

After the final round of the game, each player's board is scored and a winner is chosen. To calculate the score, the size of each terrain cluster on the board is multipled by the cumulative number of "crowns" within that cluster.

![The terminal shows each player's total score, the breakdown by terrain type, and declares Raymond the winner.](/images/scoring.png)

If the optional scoring is enabled, players also score 10 "Full Kingdom" points if their board has no empty spaces, and 5 "Centered" points if "wild" is at the center of their board.


## Future Project Goals
- Create a rules-complete version of Kingdomino that can be played in the command line.
    - Add option for 7x7 board.
    - Fix edge-case bug with "Centered Kingdom"
- Add the option to Save/Quit mid-game, then Load from a save file and continue playing.
- Create a Graphical Interface for the game
- Implement some creative rule variations, such as a tile randomizer or special player powers.