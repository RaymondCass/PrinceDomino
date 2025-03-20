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

        #Randomize the player order for the first turn
        self.table.set_current_player_pieces(Player.random_order())

        #These three parameters define how progressed the game is.
        self.current_round = 0 #put the round logic in the Game class
        self.current_tile_id = 0 #This is 0, 1, 2, or 3 depending on the tile.
            #when it rolls over to 4, it triggers a round advancement (maybe game end?)
        # todo length of game should depend on deck size
        self.final_round = 2
        self.game_is_not_over = 1

        self.temp_board = None
        self.temp_future_player_pieces = None
        self.create_save_point()

    def __str__(self):
        playstate = ""
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"


    def get_current_player(self):
        current_player = self.table.get_current_player_pieces()[self.current_tile_id]
        return current_player

    def get_current_tile(self):
        """Returns the current tile
        Note - tiles also denote player order in Princedomino,
        So the current tile indicates whose turn it is."""
        current_tile = self.table.get_current_market()[self.current_tile_id]
        return current_tile

    def get_current_round(self):
        return self.current_round


    def choose_new_tile(self, tile_id):
        future_order = self.table.get_future_player_pieces()
        future_order = list(future_order)
        if not future_order[tile_id-1]: #if no one has chosen that tile
            # the player successfully chooses the tile
            future_order[tile_id-1] = self.get_current_player()
            self.table.set_future_player_pieces(tuple(future_order))
            return 1
        else:
            return 0

    def create_save_point(self):
        """I want this function to create duplicate objects representing the current game state.
        i.e.
        A duplicate future market
        A duplicate copy of the current player's board.

        Whatever changes are made to the game, they can be undone to the most recent save point
        by calling revert_to_save_point.
        This will allow for an Undo feature to the start of the current player's turn."""
        if self.game_is_not_over == 0:
            return
        current_player = self.get_current_player()
        if current_player:
            self.temp_board = current_player.get_board().create_duplicate()
        self.temp_future_player_pieces = self.table.get_future_player_pieces()
        return

    def revert_to_save_point(self):
        """Resets the game state to where it was at the start of the round, if possible"""
        self.get_current_player().set_board(self.temp_board)
        self.table.set_future_player_pieces(self.temp_future_player_pieces)
        return


    def next_turn(self):
        """Increments the turn, and returns 1 unless the game is over"""
        self.current_tile_id += 1
        if self.current_tile_id == 4: # Check to see whether all 4 tiles have had a turn
            self._advance_round() # If yes, then advance to the next round.
        self.create_save_point()
        return self.game_is_not_over

    def _advance_round(self):
        self.current_round += 1
        if self.current_round == self.final_round:
            print("This is the start of the last round")
        if self.current_round > self.final_round:
            self.game_is_not_over = 0
            return

        self.current_tile_id = 0
        self.table.advance_tiles()
        self.table.replace_future_market(self.current_round == self.final_round)
        #unless it's the last round


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
        """Returns all player objects"""
        all_players = []
        for player_obj in cls.players.values():
            all_players.append(player_obj)
        return all_players

    @classmethod
    def get_player(cls, id):
        "returns a player specified by their ID"
        return cls.players[id]

    @classmethod
    def random_order(cls):
        random_order = cls.get_all_players()
        random.shuffle(random_order)
        if cls.player_count == 2:
            two_player_order = list(random_order)
            two_player_order.reverse()
            random_order += two_player_order #For two players, the order is a "snake." Either 0110, or 1001
        return random_order

    @classmethod
    def get_player_count(cls):
        return cls.player_count

    def get_handle(self):
        return self.handle

    def get_board(self):
        return self.board

    def set_board(self, new_board):
        """Given a Board object as input, assigns that board to the player."""
        if type(new_board) == Board.Board:
            self.board = new_board

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


    def __str__(self):
        playstate = ""
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"


    def advance_tiles(self):
        self.current_market = self.future_market
        self.current_player_pieces = self.future_player_pieces


    def replace_future_market(self, last_round = 0):
        self.future_player_pieces = (None, None, None, None)
        if last_round: #On the last round, don't draw new tiles (would probably lead to an empty-deck error)
            self.future_market = (None, None, None, None)
            return
        new_market = [self.deck.deal_tile() for n in range(4)]
        new_market.sort(key=lambda x: x.value) # sort the tiles by their value
        self.future_market = tuple(new_market)
        return

    def get_current_market(self):
        return self.current_market

    def get_future_market(self):
        return self.future_market

    def set_future_market(self, new_future_market):
        self.future_market = new_future_market


    def get_current_player_pieces(self):
        return self.current_player_pieces

    def set_current_player_pieces(self, player_order):
        if len(player_order) == 3:
            player_order.append(None)
        self.current_player_pieces = tuple(player_order)
        """Places player pieces in the current market
        (In effect, this defines the player order for the current round)"""



        #deck_type 1 is standard

    def get_future_player_pieces(self):
        return self.future_player_pieces

    def set_future_player_pieces(self, player_pieces):
        self.future_player_pieces = player_pieces





def test_variables():
    global g, p1, p2
    "lets me run some tests"
    g = Game(["Raymond", "Alex"])
    p1 = Player.get_player(0)
    p2 = Player.get_player(1)
    return

