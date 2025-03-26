import copy
import Board
import Tiles
import random


class Game:
    """Startup script:
    What are the names of the players?
    What scoring rules would you like?
    Randomized deck or standard?

    Passes these along to Table. Table creates the appropriately configured table"""
    def __init__(self, players=[], deck_type = 1, center_kingdom = False, full_kingdom = False, grid_size = 5):
        self.player_count = len(players)
        for name in players:
            Player(name, grid_size = grid_size) #default game is 5x5 grid
        self.center_kingdom = center_kingdom
        self.full_kingdom = full_kingdom

        deck = Tiles.Deck(deck_type)
        deck.shuffle()#deck_type is 1 (standard) by default

        #Each round (except for round 0), a player places a tile on their board.
        #Thus, the size of the player's board (and how many tiles would fit on it)
        # determines how many rounds there will be
        self.number_of_rounds = (pow(grid_size, 2) - 1) // 2
        tiles_needed_in_deck = self.number_of_rounds * self.player_count
        
        # A 2 player game has half as many rounds, because each player takes 2 turns per round
        if self.player_count == 2:
            self.number_of_rounds //= 2
            
        if False: #toggle to shorten game length, for testing
            self.number_of_rounds = 1

        self.current_round = 0
        self.current_turn = 0

        #Remove excess tiles from the deck
        excess_tiles = len(deck) - tiles_needed_in_deck
        if self.player_count == 3:
            # todo 3p handling
            pass #not for 3 players (until I fix those rules)
        else:
            self.discard = deck.deal_tile(excess_tiles)
            print(f"Removing {excess_tiles} tiles for a {self.player_count}-player game, "
                  f"leaving {len(deck)} in the deck")



        #set up the table
        self.table = Table(deck)
        self.table.advance_tiles()
        # Randomize the player order for the first turn
        self.table.set_current_player_pieces(Player.random_order())





        self.game_is_not_over = 1

        #These parameters allow for undoing a turn
        self.temp_board = None
        self.temp_future_player_pieces = None
        self.create_save_point()

    def __str__(self):
        playstate = ""
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"


    def get_current_player(self):
        """Uses self.current_turn as an index for table.current_player_pieces
        Whichever player is at the indexed position, it is their turn.
        Returns that player."""
        current_player = self.table.current_player_pieces[self.current_turn]
        return current_player

    def get_current_tile(self):
        """Returns the current tile
        Note - tiles also denote player order in Princedomino,
        So the current tile indicates whose turn it is."""
        current_tile = self.table.current_market[self.current_turn]
        return current_tile


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

    def try_to_place_tile(self, coord):
        """Attempts to place the current tile at the specified coordinate
        Current Tile and Current Player are determined by self.current_tile_id.

        Returns (1,"") if the placement was successful
        Return (0,Error) if the placement was unsuccessful,
        Where Error is a string explaining why the placement failed.
        """
        current_tile, current_player = self.get_current_tile(), self.get_current_player()
        col, row = coord[:1], coord[1:]

        tile_valid = current_player.board.is_tile_valid(col, row, current_tile, True)
        mssg = current_player.board.message
        if tile_valid:
            current_player.board.place_tile(col, row, current_tile, True)
            return (1, "")
        elif not tile_valid:
            return (0, f"\n'{coord}' not valid: {mssg}")
        pass

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
            self.temp_board = copy.deepcopy(current_player.board)
        self.temp_future_player_pieces = self.table.get_future_player_pieces()
        return

    def revert_to_save_point(self):
        """Resets the game state to where it was at the start of the round, if possible"""
        self.get_current_player().set_board(copy.deepcopy(self.temp_board))
        self.table.set_future_player_pieces(self.temp_future_player_pieces)
        return


    def next_turn(self):
        """Increments the turn, and returns 1 unless the game is over"""
        self.current_turn += 1
        if self.current_turn == 4: # Check to see whether all 4 tiles have had a turn
            #todo 3p handling
            self._advance_round() # If yes, then advance to the next round.
        self.create_save_point()
        return self.game_is_not_over

    def _advance_round(self):
        self.current_round += 1
        if self.current_round == self.number_of_rounds:
            print("This is the start of the last round")
        if self.current_round > self.number_of_rounds:
            self.game_is_not_over = 0
            return

        self.current_turn = 0
        self.table.advance_tiles(self.current_round == self.number_of_rounds)
        #unless it's the last round

    def score_boards(self):
        scores = {}
        for player in Player.get_all_players():
            score = player.board.score_board(self.center_kingdom, self.full_kingdom)
            scores[player] = score
        return scores


class Player:
    """Container for:
    Player's name
    Player's board
    Current Market Selection
    Future Market Selection"""
    #The class keeps a dictionary of all players to their boards.
    players = {}
    player_count = 0

    def __init__(self, player_name, board = None, grid_size = 5):

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
            self.board = Board.Board(grid_size + 2, grid_size + 2)

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

        self.current_market = (None, None, None, None)
        self.current_player_pieces = (None, None, None, None)
        self.future_market = (None, None, None, None)
        self.future_player_pieces = (None, None, None, None)

    def __str__(self):
        playstate = ""
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"


    def advance_tiles(self, last_round = 0):
        """ Advances the board state for the next round.

        'Slides' the future tiles and player markers into the current piece position,
        Then Deals 4 new tiles."""
        #Moves future pieces to the current place
        self.current_market = self.future_market
        self.current_player_pieces = self.future_player_pieces

        # Replaces the future market with new tiles
        self.future_player_pieces = (None, None, None, None)
        if last_round: #On the last round, don't draw new tiles (would probably lead to an empty-deck error)
            self.future_market = (None, None, None, None)
            return
        new_market = [self.deck.deal_tile() for n in range(4)]
        new_market.sort(key=lambda x: x.value) # sort the tiles by their value
        self.future_market = tuple(new_market)
        return


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

