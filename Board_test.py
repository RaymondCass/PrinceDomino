import unittest

import Tiles
from Board import Board


class TestBoard(unittest.TestCase):
    def test_set_cell_in_Board_class(self):
        b = Board()
        self.assertEqual(0, b.set_cell(1, 1, "2wheat"))
        try:
            s1 = Tiles.Square("wheat", 1)
            b.set_cell(1, 1, s1)
        except:
            self.fail("Failed to add a square to Board")
        self.assertEqual(0, b.set_cell(1,1,s1))


# create a board, which acts as a grid
# each board square can hold one square, e.x. "4wheat",
# These are permanent, immutable. Live on the board

# Thus, a square can be "full" or "empty"

# Empty squares should have the concept of "validity"
# A check for validity happens as follows:
# Poll two squares at once.
# 1. Both must be empty (One of the tiles is already occupied!)
# 2. Neither can be a "border square" - with an idx of 0 or "col_width/height (-1)"] (This move would exceed 5x5 grid)
# 3. Check for adjacency - one of the adjacent tiles must be of the same "suit" or "wild"(No adjacent matching suit)

# if it's all valid, prompt for confirmation. If yes, write it to the grid
# if it's not valid, return a message for which validity requirement isn't met.