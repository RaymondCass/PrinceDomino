"""
This is for board class for Princedomino
"""
import Tiles


class Grid:

    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width  # number of columns
        self.grid_height = grid_height  # number of rows
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

    def __iter__(self):
        """Iterates through the grid, returning (col, row, value) tuples"""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                yield (col, row, self.get_cell(col, row))

    def set_cell(self, col, row, value):
        self.grid[row][col] = value

    def set_full(self, col, row):
        self.grid[row][col] = 1

    def set_empty(self, col, row):
        self.grid[row][col] = 0

    def get_cell(self, col, row):
        return self.grid[row][col]

    def is_empty(self, col, row):
        return self.grid[row][col] == 0

    def four_neighbors(self, col, row):
        """
        Returns horiz/vert neighbors of cell (col, row)
        """
        ans = []
        if row > 0:
            ans.append((col, row - 1))
        if row < self.grid_height - 1:
            ans.append((col, row + 1,))
        if col > 0:
            ans.append((col - 1, row))
        if col < self.grid_width - 1:
            ans.append((col + 1, row))
        return ans


class Board(Grid):

    def __init__(self, grid_height=7, grid_width=7):
        """"""
        # create a board, which acts as a grid
        super(Board, self).__init__(grid_height, grid_width)
        self.grid_center = (self.grid_width // 2, self.grid_height // 2)
        self.grid[self.grid_center[0]][self.grid_center[1]] = 'wild'
        self.message = "All's good for now"
        self.edges = {bound: 3 for bound in ["left", "right", "top", "bottom"]}
        # TODO the edges assumes a 7x7 play space, but should be using the grid height, etc.

    def get_cell_terrain(self, col, row):
        """If the cell is a square, returns its terrain type
        If the cell is 'wild,' return 'wild'
        If the cell is empty, return None"""
        cell = self.get_cell(col, row)
        if not cell:
            return None
        elif isinstance(cell, Tiles.Square):
            cell_terrain = cell.get_terrain()
            return cell_terrain
        elif cell == 'wild':
            return 'wild'
        else:
            assert False, 'invalid cell contents.'

    def get_cell_crowns(self, col, row):
        """If the cell is a square, returns its number of crowns
        If the cell is 'home,' return 'wild'
        If the cell is empty, return None"""
        cell = self.get_cell(col, row)
        if not cell:
            return None
        elif isinstance(cell, Tiles.Square):
            cell_crowns = cell.get_crowns()
            return cell_crowns
        else:
            assert False, 'invalid cell contents.'

    def get_height_used(self, new_bound = None):
        """Return the vertical space used by comparing the two extremes.
        You can pass an upper_bound and/or a lower_bound.
        If this is more extreme, it will be used instead.

        In Princedomino, this should not exceed 5. This limit is not
        enforced by this function"""
        # TODO I don't know what these functions are for, but the edges probably don't make sense.
        # I probably just need to rethink how I'm computing the board size.
        if not new_bound:
            new_bound = self.grid_center[1]
        return max([new_bound, self.edges["bottom"]]) \
               - min([new_bound, self.edges["top"]]) \
               + 1

    def get_width_used(self, new_bound = None):
        """Return the horizontal space used by comparing the two extremes.
        You can pass a left_bound and/or a right_bound.
        If this is more extreme, it will be used instead.

        In Princedomino, this should not exceed 5. This limit is not
        enforced by this function"""
        if not new_bound:
            new_bound = self.grid_center[0]
        return max([new_bound, self.edges["right"]]) \
               - min([new_bound, self.edges["left"]]) \
               + 1

    @staticmethod
    def _square2_coords(col, row, tile):
        """A helper function that returns the coordinates (row, col) of the second square in a tile."""
        #TODO this function returns misleading information if square2 is passed in as a parameter
        offset = {'left': (-1, 0), 'up': (0, -1), 'right': (1, 0), 'down': (0, 1), }
        direction = tile.get_direction()
        col2, row2 = tuple(map(sum, zip((col, row), offset[direction])))
        return col2, row2

    def set_cell(self, col, row, value):
        """This method skips many of the validity checks on placing a tile.
        I recommend using the place_tile method.
        """
        # Update the self.edges dictionary with new bounds
        self.edges["left"] = min([col, self.edges["left"]])
        self.edges["right"] = max([col, self.edges["right"]])
        self.edges["top"] = min([row, self.edges["top"]])
        self.edges["bottom"] = max([row, self.edges["bottom"]])
        super(Board, self).set_cell(col, row, value)

    def is_square_invalid(self, col, row, square):
        """Returns a 0 if the square is valid, and a 1, 2, or 3 if not.
        If not valid, prints a reason why.

        Reasons are - (1)It's not a square object
                    - (2)Cell is full (Boards are immutable)
                    - (3)Placement would exceed a 5x5 grid
                    - (4)No adjacent tile of the same suit or 'wild'
                    """
        if not isinstance(square, Tiles.Square):  # the object is not a square
            self.message = "You can only place squares on the board. Duh."
            return 1
        elif not self.is_empty(col, row):  # if the cell is not empty
            self.message = "The cell is not empty, silly!"
            return 2
        elif self.get_width_used(new_bound=col) > 5:
            self.message = "This would exceed the 5x5 grid (on the left or right)."
            return 3
        elif self.get_height_used(new_bound=row) > 5:
            self.message = "This would exceed the 5x5 grid (on the top or bottom)."
            return 3
        else:  # determine whether there's a valid adjacent suit.
            for ncol, nrow in self.four_neighbors(col, row):
                nterrain = self.get_cell_terrain(ncol, nrow)
                if nterrain == square.get_terrain() or nterrain == "wild":
                    return 0
            return 4

    def is_tile_valid(self, col, row, tile):
        """
        Returns a 1 if the Tile is valid at the given cell;
        otherwise, returns a 0.

        The coordinates (row, col) give the desired location of tile.get_square1
        The location of tile.get_square2 adjacent to square1,
        based on tile.get_direction

        If tile is not valid, sets self.message with the reason."""
        s1, s2 = tile
        col2, row2 = self._square2_coords(col, row, tile)
        s1invalid = self.is_square_invalid(col, row, s1)
        s2invalid = self.is_square_invalid(col2, row2, s2)
        if not s1invalid and not s2invalid:
            # Either square is a valid placement.
            return 1
        elif (not s1invalid or not s2invalid) \
                and (s1invalid == 4 or s2invalid == 4):
            # One square is valid, and the other is over an empty space.
            # TODO But couldn't one square be valid for both these conditions?
            return 1
        else:
            # The tile cannot be placed at the chosen location
            return 0

    def place_tile(self, col, row, tile):
        """Checks if the Tile is valid at the location.
        If it is, places each square in the correct location, using set_cell
        Then re-centers the grid.
        """
        # TODO maybe constrain col, row, so there's no negative input silliness?
        if self.is_tile_valid(col, row, tile):
            square1, square2 = tile
            col2, row2 = self._square2_coords(col, row, tile)
            self.set_cell(col, row, square1)
            self.set_cell(col2, row2, square2)
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
            self.edges["left"] -= 1
            self.edges["right"] -= 1
        if direction == "right":
            for row in self.grid:
                rightmost = row.pop()
                row.insert(0, rightmost)
            self.edges["left"] += 1
            self.edges["right"] += 1

    def _vertical_shift(self, direction):
        """Shift entire grid vertically, either 'up' or 'down'"""
        if direction == "down":
            bottom_row = self.grid.pop()
            self.grid.insert(0, bottom_row)
            self.edges["top"] += 1
            self.edges["bottom"] += 1
        if direction == "up":
            top_row = self.grid.pop(0)
            self.grid.append(top_row)
            self.edges["top"] -= 1
            self.edges["bottom"] -= 1

    def score_board(self, center_kingdom = 0, full_kingdom = 0):
        """return the score of the board. Scoring works as follows:

        Count up connected regions. Multiply the number of tiles in a connected region
        by the number of crowns in that regions.
        Review the Breadth/Depth searches from the wildfire simulation.

        TODO: Optional Scoring
        Optional:   Score 10 points if your castle is in the center.
                    Score 5 points if your 5x5 grid contains no empty spaces.
        """
        score = dict.fromkeys(Tiles.SQUARESET, 0)
        score["empty"] = 0

        # Create a secondary Grid that tracks which tiles I've already scored.
        # The borders are automatically set to 'scored'
        scored_squares = Grid(self.grid_width, self.grid_height)
        #Handling the top and bottom edges
        scored_squares.grid[0] = [1 for n in range(self.grid_width)]
        scored_squares.grid[-1] = [1 for n in range(self.grid_width)]
        #Handling the left and right edges
        for row in range(self.grid_height):
            scored_squares.set_full(0, row)
            scored_squares.set_full(-1, row)

        # Iterate through all cells in the scored_squares Grid
        for tile in scored_squares:
            if tile[2]: # pass on tiles that have been scored (value = 1)
                continue
            col, row = tile[0], tile[1] # When encountering an unscored territory, score it
            num_connected, crowns, terrain = self._score_territory(col, row, scored_squares)

            # Multiply num_connected by num_crowns, add that to total score,
            # then continue with the iteration.
            territory_score = num_connected * crowns
            score[terrain] += territory_score

        #add bonus points (if enabled)
        if center_kingdom:
            if self.get_cell_terrain(self.grid_center[0],self.grid_center[1]) == 'wild':
                score["centered"] = 10
        if full_kingdom:
            if score["empty"] == 1:
                score["full"] = 5

        # Tally the score
        total_score = sum(score.values())

        return total_score, score





    def _score_territory(self, col, row, scored_squares):
        """Helper function for score board
        Given a specific cell (col, row),

        Updates the "scored_squares" grid, so there's no double scoring

                # When I find a tile that has not been scored, start scoring it.

            # Mark it as scored, add it to num_connected, check for crowns,
            # and check all 4 neighbors to see if
            # they're the same terrain type and
            # they haven't been scored.

        Returns num_connected, crowns, terrain"""
        scored_squares.set_full(col, row)
        terrain = self.get_cell_terrain(col, row)
        if terrain == None or terrain == "wild": # If empty or wild
            return (1, 0, "empty") # Exit the function

        num_connected = 1
        crowns = self.get_cell_crowns(col, row)
        neighbors = self.four_neighbors(col, row)
        for neighbor in neighbors:         # For unscored, adjacent tiles of the same suit:
            if scored_squares.is_empty(neighbor[0], neighbor[1]):
                if self.get_cell_terrain(neighbor[0], neighbor[1]) == terrain:
                    # Score it (and all adjacent), and add to the total.
                    add_connected, add_crowns = self._score_territory(neighbor[0], neighbor[1], scored_squares)[:2]
                    num_connected += add_connected
                    crowns += add_crowns
                    # TODO write a test for this ... I'm not sure if my recursive scorring worked
        return num_connected, crowns, terrain



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
