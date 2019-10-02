# define globals for cards
#

import random

#These are all possible squares - the suit, followed by a crown array.
SQUARESET = {
            "forest":[16,6,0,0], "wheat":[21,5,0,0], "grass":[10,2,2,0],
            "water":[12,6,0,0], "swamp":[6,2,2,0], "mine":[1,1,3,1]
            }

# define tile class
class Tile:
    """Each Domino is represented by a 2-square Tile, and has a value.
    Each square has a suit and a number of crowns.

    Possible suits are listed in the SQUARESET global variable.
    """
    
    def __init__(self, terrain1 = None, terrain2 = None, value = None):
        """Each terrain variable is a string of the suit
        prepended with the number of crowns.

        If value is not provided, it is calculated"""
        
        self.order = ["wheat","forest","water","grass","swamp","mine"]
        for terr in terrain1, terrain2:
            if terr == None:
                raise ValueError("Must provide two inputs")
            assert terr[1:] in SQUARESET, terr + " not a valid suit"
            assert SQUARESET[terr[1:]][int(terr[0])] is not 0, (
                terr + " has too many crowns")


        tile1, tile2 = self.sort_squares(terrain1, terrain2)
        self.terrain1 = tile1
        self.terrain2 = tile2
        self.suit1 = tile1[1:]
        self.suit2 = tile2[1:]
        self.crown1 = int(tile1[0])
        self.crown2 = int(tile2[0])

        #calculate value (if value provided, use that instead).
        self.value = self.calculate_value(value)


    def __str__(self):
        return ("[" + self.terrain1 + "|" + self.terrain2 + "]") 

    def get_square1(self):
        return self.terrain1

    def get_square2(self):
        return self.terrain2

    def get_suit1(self):
        return self.suit1

    def get_suit2(self):
        return self.suit2
    
    def get_crowns1(self):
        return self.crown1

    def get_crowns2(self):
        return self.crown2

    def get_value(self):
        return self.value

    def calculate_value(self, value = None):
        if value:
            return int(value)
        value = 50 * (self.crown1 + self.crown2)
        value += self.order.index(self.suit2)
        if self.suit1 == self.suit2:
            return value
        value += (( 1 + self.order.index(self.suit1)) * 7)
        return value
        
    def sort_squares(self, terrain1, terrain2):
        "Standardizes order for 2 tiles"

        #If one square has more growns, it should be terrain1
        crowns1, crowns2 = terrain1[0], terrain2[0]
        if crowns2 > crowns1:
            return (terrain2, terrain1)
        if crowns1 > crowns2:
            return (terrain1, terrain2)

        #If crowns are the same, sort based on the suit order
        if self.order.index(terrain1[1:]) > self.order.index(terrain2[1:]):
            return (terrain2, terrain1)
        else:
            return (terrain1, terrain2)
            

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define deck class
class Deck:
    def __init__(self, random = True, deck = None):

        if deck:
            self.deck = deck
        elif random:
            pass
        else:
            self.deck = self._standard_deck()
            
    def _standard_deck(self):
        """Generates the standard deck for KingDomino, courtesy of
        https://github.com/RuPaulsDataRace/Kingdomino-For-Queens
        """
        standeck = []
        f = open("./Kingdomino-For-Queens/kingdomino.csv", "r")
        lines = f.readlines()
        dominos = [d.split(",") for d in lines[1:]]
        for dom in dominos:
            tile = Tile(dom[7], dom[8][:-1], dom[0])
            standeck.append(tile)
        return standeck

    def contains(self, tile):
        """Returns wheather an equivalent tile appears in deck
        Note: This looks for a string representation, not the actual object.
        """
        match = str(tile)
        for domino in self.deck:
            if str(domino) == match:
                return True
        return False

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        string = " \n".join([str(t) for t in self.deck])
        return "Dominos in deck are: \n" + string
