import Board
import Tiles
import random


class Game:
    """Startup script:
    What are the names of the players?
    What scoring rules would you like?
    Randomized deck or standard?

    Passes these along to Table. Table creates the appropriately configured table"""
    def __init__(self, players=[], deck_type = 1, center_kingdom = 0, full_kingdom = 0):
        self.player_count = len(players)
        for name in players:
            Player(name)
        self.center_kingdom = center_kingdom
        self.full_kingdom = full_kingdom

        deck = Tiles.Deck(deck_type) #deck_type is 1 (standard) by default
        if self.player_count == 2:
            pass #todo halve the deck
        self.table = Table(deck)
        self.initial_player_order = Player.random_order()
        self.table.set_current_player_pieces(self.initial_player_order)

        #These three parameters define how progressed the game is.
        self.current_round = 0 #put the round logic in the Game class
        self.current_tile_id = 0 #This is 0, 1, 2, or 3 depending on the tile.
            #when it rolls over to 4, it triggers a round advancement (maybe game end?)
        self.final_round = 2
        self.game_is_not_over = 1

    def __str__(self):
        playstate = ""
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"

    def get_initial_player_order(self):
        return self.initial_player_order

    def get_current_player(self):
        current_player_id = self.table.get_current_player_pieces()[self.current_tile_id]

        if current_player_id != None:
            return Player.get_player(current_player_id)
        else:
            return None

    def get_current_tile(self):
        """Returns the current tile
        Note - tiles also denote player order in Princedomino,
        So the current tile indicates whose turn it is."""
        current_tile = self.table.get_current_market()[self.current_tile_id]
        return current_tile

    def get_future_tiles(self):
        return self.table.get_future_market()

    def get_current_round(self):
        return self.current_round

    def next_turn(self):
        """Increments the turn, and returns 1 unless the game is over"""
        self.current_tile_id += 1
        if self.current_tile_id == 4:
            self.next_round()
        return self.game_is_not_over
    #todo returns 0 if the game is over

    def next_round(self):
        self.current_round += 1
        if self.current_round == self.final_round:
            print("This is the start of the last round")
        if self.current_round > self.final_round:
            print ("The game is over, please stop playing")
            self.game_is_not_over = 0
            return

        self.current_tile_id = 0
        self.table.advance_market()
        c_market = [str(i) for i in self.table.get_current_market()]
        print(f"Advancing the market... current market is now{c_market}")

        self.table.replace_future_market(self.current_round == self.final_round)
        #unless it's the last round
        f_market = [str(i) for i in self.table.get_future_market()]
        print(f"Drawing new tiles... future market is now{f_market}")

        print(f"Start of round {self.current_round}\n")



    #pass
    #Table(4,1,0,0)
    #players = input("How many players?")

class Player:
    """Container for:
    Player's name
    Player's board
    Current Market Selection
    Future Market Selection"""
    #The class keeps a dictionary of all players to their boards.
    players = {}
    player_count = 0


    def __init__(self, player_name, board = None):

        self.current_round_selection = (None, None)
        self.future_round_selection = [None, None]

        #Each player has a unique id.
        self.handle = player_name
        self.id = Player.player_count
        Player.player_count += 1
        Player.players[self.id] = self

        #You can assign a player a board. Otherwise, they are given a new one
        if board:
            assert isinstance(board, Board.Board), 'Provided boards must be an instance of the Board class'
            self.board = board
        else:
            self.board = Board.Board()

    @classmethod
    def get_all_players(cls):
        """Returns the ids of all players"""
        all_players = []
        for player_id in cls.players:
            all_players.append(player_id)
        return all_players

    @classmethod
    def get_player(cls, id):
        "returns a player specified by their ID"
        return cls.players[id]

    @classmethod
    def random_order(cls):
        if cls.player_count == 2:
            two_player_order = [0, 1, 1 ,0], [1, 0, 0, 1]
            return random.choice(two_player_order)
        random_order = cls.get_all_players()
        random.shuffle(random_order)
        return random_order

    def get_handle(self):
        return self.handle

    def get_board(self):
        return self.board

    def get_current_round_selection(self, second=0):
        """"Returns the id of the tile selected for the current round
        Pass "1" as the optional parameter to get the 2nd value, in 2-player mode.
        """
        return self.current_round_selection[second]

    def get_future_round_selection(self, second=0):
        """"Returns the id of the tile selected for the future round
        Pass "1" as the optional parameter to get the 2nd value, in 2-player mode.
        """
        return self.future_round_selection[second]

    def set_future_round(self, first_selection = None, second_selection = None):
        if first_selection:
            self.future_round_selection[0] = first_selection
        if second_selection:
            self.future_round_selection[1] = second_selection

    def advance_round(self):
        """Makes the present becomes the past, and the future becomes unknown"""
        self.current_round_selection = self.future_round_selection
        self.future_round_selection = (None, None)

    def new_game(self):
        pass





class Table:
    """A container for:
    The deck class being used.
    The 4-8 tiles viewable on the table.
    The primary Draw methods for displaying the game
    The buttons that a player clicks to rotate the tile

    The game board should be pretty static. You only need to refresh when
    A tile is placed, rotated, or a choice is made.

    Also contains the rules for the game.
    """
    def __init__(self, deck):
        self.deck = deck
        self.deck.shuffle()

        self.current_market = (None, None, None, None)
        self.current_player_pieces = (None, None, None, None)
        self.future_market = (None, None, None, None)
        self.future_player_pieces = (None, None, None, None)

        self.replace_future_market()

    def advance_market(self):
        self.current_market = self.future_market
        #self.current_player_pieces = self.future_player_pieces

    def replace_future_market(self, last_round = 0):
        self.future_player_pieces = (None, None, None, None)
        if last_round: #On the last round, don't draw new tiles (would probably lead to an empty-deck error)
            self.future_market = (None, None, None, None)
            return
        new_market = [self.deck.deal_tile() for n in range(4)]
        new_market.sort(key=lambda x: x.value) # sort the tiles by their value
        self.future_market = tuple(new_market)
        return

    def get_current_player_pieces(self):
        return self.current_player_pieces

    def get_current_market(self):
        return self.current_market

    def get_future_market(self):
        return self.future_market

    def set_current_player_pieces(self, player_order):
        if len(player_order) == 3:
            player_order.append(None)
        self.current_player_pieces = tuple(player_order)
        """Places player pieces in the current market
        (In effect, this defines the player order for the current round)"""



        #deck_type 1 is standard

# TODO A "turn" is as follows: 1. Player places a tile, 2. Player chooses a tile
# The Table class contains the GUI needed to interact. Handles visuals and user input.

if __name__ == "__main__":
    Game()

def test_variables():
    global g, p1, p2
    "lets me run some tests"
    g = Game(["Raymond", "Colleen"])
    p1 = Player.get_player(1)
    p2 = Player.get_player(2)
    return

