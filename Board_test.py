import unittest

from Tiles import Deck, Square
from Board import Board


class TestBoard(unittest.TestCase):
    def test_set_cell(self):
        b = Board()
        self.assertRaises(AssertionError, Square, "wheat", 2)
        try:
            s1 = Square("wheat", 1)
            b.set_cell(1, 1, s1)
        except:
            self.fail("Failed to add a square to Board")
        self.assertEqual(0, b.is_empty(1,1))

    def test_square2_coords(self):
        d = Deck()
        t1 = d.deal_tile()
        self.assertEqual(Board._square2_coords(2, 2, t1), (3, 2))
        t1.rotate('clockwise')
        self.assertEqual(Board._square2_coords(3, 3, t1), (3, 4))
        t1.rotate('clockwise')
        self.assertEqual(Board._square2_coords(2, 2, t1), (1, 2))
        t1.rotate('clockwise')
        self.assertEqual(Board._square2_coords(1, 2, t1), (1, 1))

    def test_is_square_invalid(self):
        b = Board()
        s1, s2 = Square("grass", 0), Square("grass", 0)
        s3, s4 = Square("wheat", 0), Square("grass", 1)
        self.assertEqual(b.is_square_invalid(3, 3, s1), 1, "Cell is not empty")
        self.assertEqual(b.is_square_invalid(3, 2, s1), 0, "Cell is empty, 'wild' is adjacent")
        b.set_cell(3,2,s1)
        self.assertEqual(b.is_square_invalid(3, 1, s2), 0, "Cell is empty, 'grass' is adjacent")
        self.assertEqual(b.is_square_invalid(3, 2, s2), 1, "Cell is not empty")
        b.set_cell(3,1, s2)
        self.assertEqual(b.is_square_invalid(0,3,s4), 3, "No adjacent tiles")
        self.assertEqual(b.is_square_invalid(1, 3, s3), 3, "No adjacent lookalikes")
        self.assertEqual(b.is_square_invalid(2, 3, s4), 0, "Next to 'wild'")
        b.set_cell(2,3,s4)
        self.assertEqual(b.is_square_invalid(1, 3, s3), 3, "No adjacent lookalikes")
        b.set_cell(3, 4, s3)
        b.set_cell(3, 5, s3)
        print(b)
        self.assertEqual(b.is_square_invalid(3, 6, s3), 2, "Would exceed 5x5 tile")
        print(b)
        b.set_cell(6, 3, s3)
        self.assertEqual(b.is_square_invalid(1, 3, s2), 2, "Would exceed 5x5 tile")

    def test__center(self):
        b = Board()
        d = Deck()
        t1 = d.deal_tile()
        b.place_tile(1, 3, t1)
        self.assertEqual(1, b.is_empty(1, 3), "The previously placed tile has slid over")
        self.assertEqual(0, b.is_empty(2, 3), "The previously placed tile slid over 1")
        self.assertEqual(0, b.is_empty(4, 3), "This tile would be empty, but is now not")
        self.assertEqual(1, b.is_empty(5, 3), "This tile, however, is still empty")
        b.place_tile(5, 3, t1)
        self.assertEqual(0, b.is_empty(1, 3), "This tile is now full")
        self.assertEqual(1, b.is_empty(6, 3), "The edge tile still should be empty")


    def test_set_tile(self):
        # TODO rewrite these tests to account and check for the _center method.
        b = Board()
        d = Deck(True)
        t1 = d.deal_tile()
        self.assertEqual(b.is_tile_valid(2, 3, t1), 0, "This should overlap home")
        self.assertEqual(b.is_tile_valid(1, 3, t1), 1, "This should not overlap home")
        try:
            b.place_tile(1, 3, t1)
        except:
            self.fail("Could not place the tile (t1)")
        t2 = d.deal_tile()
        t2.rotate('counterclockwise')
        self.assertEqual(b.is_tile_valid(1, 2, t2), 1)
        try:
            b.place_tile(1, 2, t2)
            print (b)
        except:
            self.fail("Could not place the tile (t2)")





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