"""
This contains the Tile and Deck classes for Peasantdomino.
"""
import random

# These are all possible squares - the suit, followed by a crown array.
SQUARESET = {
    "forest": [16, 6, 0, 0], "wheat": [21, 5, 0, 0], "grass": [10, 2, 2, 0],
    "water": [12, 6, 0, 0], "swamp": [6, 2, 2, 0], "mine": [1, 1, 3, 1]
}


class Square:
    def __init__(self, terrain, crowns):
        assert terrain in SQUARESET, terrain + " not a valid terrain type"
        assert SQUARESET[terrain][int(crowns)] is not 0, (
                    str(crowns) + " is not a valid number of crowns for " + str(terrain))
        self.terrain = str(terrain)
        self.crowns = int(crowns)

    def __str__(self):
        return str(self.crowns) + self.terrain

    def get_terrain(self):
        return self.terrain

    def get_crowns(self):
        return self.crowns

    @staticmethod
    def is_valid_square(terrain, crowns):
        """A method to say whether the provided square could exist
        (according to SQUARESET)

        TODO Write this (or delete it if I decide I don't need it"""
        pass

    @staticmethod
    def all_squares():
        """Returns list of all possible square objects"""
        # Iterate through SQUARESET to create all possible squares
        squares = []
        for terrain in SQUARESET:
            for crowns in [0, 1, 2, 3]:
                for n in range(SQUARESET[terrain][crowns]):
                    squares.append(Square(terrain, crowns))
        assert len(squares) % 2 == 0, "Can't have an odd number of squares. Did you modify SQUARESET?"
        return squares

# define tile class
class Tile:
    """Each Domino is represented by a 2-square Tile, which has a value and direction.
    Each square has a number of crowns and a suit. For example, "0wheat" or "2swamp"
    Possible suits are "forest", "wheat", "grass", "water", "swamp", or "mine".

    The value, if not provided, will be calculated using a function that adheres to the valuation of the base cards
    The direction can be "left", "right", "up", or "down", and defaults to "left".
    """

    def __init__(self, square1=None, square2=None, value=None):
        """Each terrain variable is a Square object

        If the tile value is not provided, it is calculated"""

        self.order = ["wheat", "forest", "water", "grass", "swamp", "mine"]
        if square1 is None or square2 is None:
            raise ValueError("Must provide two squares as input")
        assert square1 != square2, "Can't use the same square twice"

        tile1, tile2 = self.sort_squares(square1, square2)

        self.square1 = tile1
        self.square2 = tile2
        self.direction = "right"

        # calculate value (if value provided, use that instead).
        self.value = self.calculate_value(value)

    def __str__(self):
        return "[" + str(self.square1) + "|" + str(self.square2) + "]"

    def __iter__(self):
        yield self.square1
        yield self.square2

    def print_details(self):
        print("Tile = " + str(self) + "\n Value = " + str(self.value) + "\n Direction = " + self.direction)

    def get_square1(self):
        return self.square1

    def get_square2(self):
        return self.square2

    def get_value(self):
        return self.value

    def _set_value(self, new_value):
        self.value = new_value

    def get_direction(self):
        return self.direction

    def rotate(self, spin):
        """Rotate the card's direction either 'clockwise' or 'counterclockwise'. Default is clockwise.

        Directions cycle from 'left' to 'up' to 'right' to 'down'."""
        rotate = ['left', 'up', 'right', 'down']
        if spin == "counterclockwise":
            mult = -1
        else:
            mult = 1
        self.direction = rotate[(rotate.index(self.direction) + mult) % 4]

    def calculate_value(self, value=None):
        if value:
            return int(value)
        value = 50 * (self.square1.get_crowns() + self.square2.get_crowns())
        value += self.order.index(self.square2.get_terrain())
        if self.square1.get_terrain() == self.square2.get_terrain():
            return value
        value += ((1 + self.order.index(self.square1.get_terrain())) * 7)
        return value

    def sort_squares(self, square1, square2):
        "Standardizes order for 2 tiles"

        # If one square has more crowns, it should be terrain1
        if square2.get_crowns() > square1.get_crowns():
            return square2, square1
        if square1.get_crowns() > square2.get_crowns():
            return square1, square2

        # If crowns are the same, sort based on the suit order
        if self.order.index(square1.get_terrain()) > self.order.index(square2.get_terrain()):
            return square2, square1
        else:
            return square1, square2

    # def draw(self, canvas, pos):
    #     card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
    #                 CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
    #     canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
    #                       CARD_SIZE)


# define deck class
class Deck:
    def __init__(self, standard=False, deck=None):
        """
        A deck is a list of kingdomino Tile objects.
        It has standard deck operations, such as dealing and shuffling.

        Calling Deck with no parameters will return a deck of randomly generated tiles.
        To use the standard deck of tiles, pass (standard = True).
        To use a specific deck, pass (deck = [list_of_tiles])
        """
        if deck:
            self.deck = deck
        elif standard:
            self.deck = self._standard_deck()
        else:
            self.deck = self._random_deck()

    @staticmethod
    def _standard_deck():
        """Generates the standard deck for KingDomino, courtesy of
        https://github.com/RuPaulsDataRace/Kingdomino-For-Queens
        """
        standeck = []
        with open("./Kingdomino-For-Queens/kingdomino.csv", "r") as f:
            lines = f.readlines()
        dominos = [d.split(",") for d in lines[1:]]
        for domino in dominos:
            tile = Tile(Square(domino[1],domino[5]),
                        Square(domino[3],domino[6]), domino[0])
            standeck.append(tile)
        return standeck

    @staticmethod
    def _random_deck():
        squares = Square.all_squares()
        # Randomly combine pairs of squares into a tile.
        random.shuffle(squares)
        randeck = []
        while len(squares) != 0:
            s1, s2 = squares.pop(), squares.pop()
            tile = Tile(s1, s2)
            randeck.append(tile)
        # Standardize the values of the tiles
        valuedeck = sorted(randeck, key=Tile.get_value)
        for c in range(len(valuedeck)):
            valuedeck[c]._set_value(c + 1)
        return randeck

    def contains(self, tile):
        """Returns whether an equivalent tile appears in deck
        Note: This looks for a string representation, not the actual object.
        """
        for domino in self.deck:
            if str(domino) == str(tile):
                return True
        return False

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_tile(self):
        return self.deck.pop()

    def __str__(self):
        string = " \n".join([str(d) for d in self.deck])
        return "Dominos in deck are: \n" + string
