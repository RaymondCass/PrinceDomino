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
            for value in row:
                r += "{0:^7}".format(str(value))
            print_string += r + "\n\n\n"
        return print_string

    def set_cell(self, row, col, value):
        self.grid[col][row] = value

    def get_cell(self, row, col):
        return self.grid[col][row]

    def is_empty(self, row, col):
        return self.grid[col][row] == 0

    def four_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col)
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self.grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self.grid_width - 1:
            ans.append((row, col + 1))
        return ans


class Board(Grid):

    def __init__(self, grid_height=7, grid_width=7):
        """"""
        # create a board, which acts as a grid
        super(Board, self).__init__(grid_height, grid_width)
        self.grid[self.grid_height // 2][self.grid_width // 2] = "wild"
        self.message = "All's good for now"
        self.edges = {bound: 3 for bound in ["left", "right", "top", "bottom"]}

    def get_cell_terrain(self, row, col):
        """If the cell is a square, returns its terrain type
        If the cell is 'home,' return 'wild'
        If the cell is empty, return None"""
        cell = self.get_cell(row, col)
        if not cell:
            return None
        elif isinstance(cell, Tiles.Square):
            cell_terrain = cell.get_terrain()
            return cell_terrain
        elif cell == 'wild':
            return 'wild'
        else:
            assert False, 'invalid cell contents.'

    def get_height_used(self, upper_bound=3, lower_bound=3):
        """Return the vertical space used by comparing the two extremes.
        You can pass an upper_bound and/or a lower_bound.
        If this is more extreme, it will be used instead.

        In Peasantdomino, this should not exceed 5. This limit is not
        enforced by this function"""
        return max([lower_bound, self.edges["bottom"]]) \
               - min([upper_bound, self.edges["top"]]) \
               + 1

    def get_width_used(self, left_bound=3, right_bound=3):
        """Return the horizontal space used by comparing the two extremes.
        You can pass a left_bound and/or a right_bound.
        If this is more extreme, it will be used instead.

        In Peasantdomino, this should not exceed 5. This limit is not
        enforced by this function"""

        return max([right_bound, self.edges["right"]]) \
               - min([left_bound, self.edges["left"]]) \
               + 1

    @staticmethod
    def _square2_coords(row, col, tile):
        """A helper function that returns the coordinates (row, col) of the second square in a tile."""
        offset = {'left': (-1, 0), 'up': (0, -1), 'right': (1, 0), 'down': (0, 1), }
        direction = tile.get_direction()
        row2, col2 = tuple(map(sum, zip((row, col), offset[direction])))
        return row2, col2

    def set_cell(self, row, col, value):
        """This method skips many of the validity checks on placing a tile.
        I recommend using the place_tile method.
        """
        # Update the self.edges dictionary with new bounds
        self.edges["left"] = min([col, self.edges["left"]])
        self.edges["right"] = max([col, self.edges["right"]])
        self.edges["top"] = min([row, self.edges["top"]])
        self.edges["bottom"] = max([row, self.edges["bottom"]])
        super(Board, self).set_cell(row, col, value)

    def is_square_invalid(self, square, row, col):
        """Returns a 0 if the square is valid, and a 1, 2, or 3 if not.
        If not valid, prints a reason why.
            self.set_cell(row, col, square1)
            self.set_cell(row2, col2, square2)
            # TODO Calculate new edges, before centering.
            min()

        Reasons are - (1)Cell is full (Boards are immutable)
                    - (2)Placement would exceed 5x5 grid (There must be a x1 border around the board)
                    - (3)No adjacent tile of the same suit or 'wild'"""

        # TODO rewrite this function.
        assert self.is_empty(row, col), "Board is immutable. You may only set empty cells"
        assert isinstance(value, Tiles.Square), str(value) + "is not a Tiles.Square object"
        self._center()
        return 1

    else:
        return 0

    def is_tile_valid(self, row, col, tile):
        """
        Returns a 1 if the Tile is valid at the given cell;
        otherwise, returns a 0.

        The coordinates (row, col) give the desired location of tile.get_square1
        The location of tile.get_square2 adjacent to square1,
        based on tile.get_direction

        If tile is not valid, sets self.message with the reason."""
        s1, s2 = tile
        row2, col2 = self._square2_coords(row, col, tile)
        s1invalid = self.is_square_invalid(row, col, s1)
        s2invalid = self.is_square_invalid(row2, col2, s2)
        if not s1invalid and not s2invalid:
            # Either square is a valid placement.
            return 1
        elif (not s1invalid or not s2invalid) \
                and (s1invalid == 3 or s2invalid == 3):
            # One square is valid, and the other is over an empty space.
            return 1
        else:
            # The tile cannot be placed at the chosen location
            return 0

    def place_tile(self, row, col, tile):
        """Checks if the Tile is valid at the location.
        If it is, places each square in the correct location, using set_cell
        Then re-centers the grid.
        """
        if self.is_tile_valid(row, col, tile):
            # TODO Is_tile_valid must make sure the 5x5 isn't exceeded
            square1, square2 = tile
            row2, col2 = self._square2_coords(row, col, tile)

            self.set_cell(row, col, square1)
            self.set_cell(row2, col2, square2)
            # TODO Calculate new edges, before centering.
            min()

            self._center()
            return 1
        else:
            return 0

    def _center(self):
        """Keeps the board centered, so it doesn't need to do
        fancy wrapping things or mutatable edges.

        May be useful to keep a binary row/column counter.
        ex. Rows:0011110, Col:0011100

        This function determines whether to bump a 0 row/column to the other side."""
        left_margin = self.edges["left"]
        right_margin = self.grid_width - 1 - self.edges["right"]
        if left_margin > (right_margin + 1):  # slide to the left
            self._horizontal_shift("left")
        elif right_margin > (left_margin + 1):  # slide to the right
            self._horizontal_shift("right")

        top_margin = self.edges["top"]
        bottom_margin = self.grid_height - 1 - self.edges["bottom"]
        if top_margin > (bottom_margin + 1):  # slide toward the top
            self._vertical_shift("up")
        elif bottom_margin > (top_margin + 1):  # slide toward the bottom
            self._vertical_shift("down")

    def _horizontal_shift(self, direction):
        """Shift entire grid horizontally, either 'left' or 'right'"""
        if direction == "left":
            for row in self.grid:
                leftmost = row.pop(0)
                row.append(leftmost)
        if direction == "right":
            for row in self.grid:
                rightmost = row.pop()
                row.insert(0, rightmost)

    def _vertical_shift(self, direction):
        """Shift entire grid vertically, either 'up' or 'down'"""
        if direction == "down":
            bottom_row = self.grid.pop()
            self.grid.insert(0, bottom_row)
        if direction == "up":
            top_row = self.grid.pop(0)
            self.grid.append(top_row)

    def score_board(self):
        """return the score of the board. Scoring works as follows:

        Count up connected regions. Multiply the number of tiles in a connected region
        by the number of crowns in that regions.
        Review the Breadth/Depth searches from the wildfire simulation.

        Optional:   Score 10 points if your castle is in the center.
                    Score 5 points if your 5x5 grid contains no empty spaces.
        """
        # TODO Write the scoring method. Using recursion, as in the Zombie Apocalypse sim

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
    pass
