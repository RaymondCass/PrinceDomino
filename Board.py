"""
This is for board class for Peasantdomino
"""
import Tiles


class Grid:

    def __init__(self, grid_height, grid_width):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = [[0 for n in range(grid_width)]
                     for m in range(grid_height)]

    def __str__(self):
        print_string = ""
        for row in self.grid:
            r = ""
            for num in row:
                r += "{0:^7}".format(num)
            print_string += r + "\n\n\n"
        return print_string

    def set_cell(self, row, col, value):
        self.grid[row][col] = value

    def get_cell(self, row, col):
        return self.grid[row][col]

    def is_empty(self, row, col):
        return self.grid[row][col] == 0


class Board(Grid):

    def __init__(self, grid_height=7, grid_width=7):
        """"""
        # create a board, which acts as a grid
        super(Board, self).__init__(grid_height, grid_width)
        self.grid[self.grid_height // 2][self.grid_width // 2] = "wild"

    def set_cell(self, row, col, value):
        if self.is_square_invalid(row, col, value):
            return 0
        super(Board, self).set_cell(row, col, value)
        self._center()
        return 0

    def is_tile_valid(self, tile, row, col):
        """
        Returns a 1 if the Tile is valid at the given cell; otherwise, returns a 0.

        The coordinates (row, col) give the desired location of tile.get_square1
        The location of tile.get_square2 adjacent to square1, based on tile.get_direction

        Prints a reason to the console if the tile is not valid."""
        pass
        # basically, just call is_square_valid for each tile consecutively.
        # however, only one square needs to be adjacent.

    def place_tile(self, tile, row, col):
        """Checks if the Tile is valid at the location.
        If it is, places each square in the correct location, using set_cell
        """

    def is_square_invalid(self, square, row, col):
        """Returns a 0 if the square is valid, and a 1, 2, or 3 if not.
        If not valid, prints a reason why.

        Reasons are - (1)Cell is full (Boards are immutable)
                    - (2)Placement would exceed 5x5 grid (There must be a x1 border around the board)
                    - (3)No adjacent tile of the same suit or 'wild'"""
        assert self.is_empty(row, col), "Board is immutable. You may only set empty cells"
        assert isinstance(value, Tiles.Square), str(value) + "is not a Tiles.Square object"

    def _center(self):
        """Keeps the board centered, so it doesn't need to do fancy wrapping things or mutatable edges.

        May be useful to keep a binary row/column counter. ex. Rows:0011110, Col:0111000

        This function determines whether to bump a 0 row/column to the other side."""

    def draw(self):
        """Draws the board in one of 4 quadrants"""
        pass

# Empty squares should have the concept of "validity"
# A check for validity happens as follows:
# Poll two squares at once.
# 1. Both must be empty (One of the tiles is already occupied!)
# 2. Neither can be a "border square" - with an idx of 0 or "col_width/height (-1)"] (This move would exceed 5x5 grid)
# 3. Check for adjacency - one of the adjacent tiles must be of the same "suit" or "wild"(No adjacent matching suit)

# if it's all valid, prompt for confirmation. If yes, write it to the grid
# if it's not valid, return a message for which validity requirement isn't met.


if __name__ == "__main__":
    b = Board()
    print(b)
    b = Grid(4, 6)
    b.grid[2][4] = "4wheat"
