import copy
import Board
import Tiles
import random


class Game:
    """Game contains the logic and data structures to play a game of PrinceDomino.
    It has various functions that allow for manipulating the game state.

    Player names and boards are stored in Player objects,
    while cards in play and turn order are stored in a Table object."""
    def __init__(self, players: list, deck_type = 1, center_kingdom = False, full_kingdom = False, grid_size = 5):

        self.player_count = len(players)

        self.num_player_pieces = self.player_count
        if self.num_player_pieces == 2:
            self.num_player_pieces *= 2

        for name in players:
            Player(name, grid_size = grid_size) #default game is 5x5 grid

        self.center_kingdom, self.full_kingdom = center_kingdom, full_kingdom

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
            self.number_of_rounds = 2

        self.current_round = 0
        self.current_turn = 0 # This parameter is used as an index for the table.current_player_pieces to
                              # to determine who the current player is.

        #Remove excess tiles from the deck
        excess_tiles = len(deck) - tiles_needed_in_deck
        self.discard = deck.deal_tile(excess_tiles)
        print(f"Removing {excess_tiles} tiles for a {self.player_count}-player game, "
              f"leaving {len(deck)} in the deck")

        #set up the table
        self.table = Table(deck, self.num_player_pieces)
        self.table.advance_tiles()
        # Randomize the player order for the first turn.
        # If 2 players, each player gets 2 turns in snake formation. This is a house rule but I like it.
        self.table.current_player_pieces = Player.random_order(snake = Player.player_count == 2)

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
        """Return's the player whose turn it is.
        """
        current_player = self.table.current_player_pieces[self.current_turn]
        return current_player

    def get_current_tile(self):
        """Returns the current tile
        """
        current_tile = self.table.current_market[self.current_turn]
        return current_tile


    def try_to_choose_new_tile(self, tile_id):
        """
        Move handler for the choose tile phase of a turn.
        Attempts to have the current player choose the tile_id tile from the future market.
        Returns 1 if successful, or 0 if unsuccessful (because the tile has already been claimed).
        """
        future_order = self.table.future_player_pieces
        future_order = list(future_order)
        if not future_order[tile_id-1]: #if no one has chosen that tile
            # the player successfully chooses the tile
            future_order[tile_id-1] = self.get_current_player()
            self.table.future_player_pieces = tuple(future_order)
            return 1
        else:
            return 0

    def try_to_place_tile(self, player_input):
        """Handler for the tile-placement phase of a player's turn.
        Assumes that player_input is a potentially valid move (an existing coordinate, or a "P" or "R" action).

        Returns (n, Message)
        n = 1 if the game can advance, or 0 if further input for the turn is needed.
        The game can advance if the tile was successfully placed, or if the player validly passed.
        Message is "" if the tile was successfully placed.
        Otherwise, it provides context for why the placement was unsuccessful.
        """
        current_tile, current_player = self.get_current_tile(), self.get_current_player()

        # Rotation Handling
        if player_input == "R":
            current_tile.rotate()
            return (0, "Tile Rotated") # Rotating the tile does not advance the game state.

        # Pass Handling
        elif player_input == "P":
            # Passing (if valid) advances the game state.
            return (1, "You have passed on placing your tile. (This should only be allowed if you have no valid moves, "
                       "but that check has not yet been implemented.)")
            #todo implement passing, don't just allow it whenever

        col, row = player_input[:1], player_input[1:]

        tile_valid = current_player.board.is_tile_valid(col, row, current_tile, True)
        mssg = current_player.board.message

        if tile_valid:
            current_player.board.place_tile(col, row, current_tile, True)
            return (1, "")
        elif not tile_valid:
            return (0, f"\n'{player_input}' not valid: {mssg}")

    def create_save_point(self):
        """When called at the start of a turn, creates a copy of the current player's board and the future market.
        These can be used to revert the game state, or 'undo' the current player's turn.

        WARNING: This does not create a complete copy of the Game, and can not be used to create an arbitrary save point.
        It only works within the scope of a player's current turn.
        """
        if self.game_is_not_over == 0:
            return
        current_player = self.get_current_player()
        if current_player:
            self.temp_board = copy.deepcopy(current_player.board)
        self.temp_future_player_pieces = self.table.future_player_pieces
        return

    def revert_to_save_point(self):
        """Resets the game state to where it was at the start of the turn.

        WARNING: This can only revert to the start of a turn, and only if create_save_point was called.
        The scope is limited to a player's current turn.
        """
        self.get_current_player().set_board(copy.deepcopy(self.temp_board))
        self.table.future_player_pieces = self.temp_future_player_pieces
        return


    def next_turn(self):
        """Increments the turn, with necessary game upkeep.
        Returns 1 if the game is ongoing.
        Reutnrs 0 if the game is over.
        """
        self.current_turn += 1
        if self.current_turn == self.num_player_pieces: # Check to see whether all tiles have had a turn
            self._advance_round() # If yes, then advance to the next round.
        self.create_save_point()
        return self.game_is_not_over

    def _advance_round(self):
        """Helper function for next_turn.
        """
        self.current_round += 1
        if self.current_round == self.number_of_rounds:
            print("This is the start of the last round")
        if self.current_round > self.number_of_rounds:
            self.game_is_not_over = 0
            return

        self.current_turn = 0
        self.table.advance_tiles(self.current_round == self.number_of_rounds)      #unless it's the last round


    def score_boards(self):
        """Returns a dictionary of all the player's current scores.
        The structure of the dictionary is:

        {Player:[total score, score_details], ...}
        Where Player is a Player object, total score is an int, and score_details is another dictionary.
        """
        scores = {}
        for player in Player.get_all_players():
            score = player.board.score_board(self.center_kingdom, self.full_kingdom)
            scores[player] = score
        return scores


class Player:
    """Container for a player's name and board,
    with several class methods for accessing all players.
    """
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
            self.board = Board.Board(grid_size, grid_size)

    @classmethod
    def get_all_players(cls):
        """Returns a list of all player objects"""
        all_players = []
        for player_obj in cls.players.values():
            all_players.append(player_obj)
        return all_players

    @classmethod
    def get_player(cls, id):
        "returns a player specified by their ID"
        return cls.players[id]

    @classmethod
    def random_order(cls, snake = False):
        """ Returns a list of players in a random order.
        If Snake is True, appends a reversed copy of the list to itself before returning.
        Eg, for players A, B, C, it might return [C, A, B, B, A, C]
        This is useful for "snake drafts."
        """
        random_order = cls.get_all_players()
        random.shuffle(random_order)
        if snake:
            reverse_order = list(random_order)
            reverse_order.reverse()
            random_order += reverse_order #For two players, the order is a "snake." Either 0110, or 1001
        return random_order

    @classmethod
    def get_player_count(cls):
        return cls.player_count


    def set_board(self, new_board):
        """Given a Board object as input, assigns that board to the player."""
        if type(new_board) == Board.Board:
            self.board = new_board

    def new_game(self):
        """If I add the ability to play multiple games in a row
        I might need to purge the Player class to prevent 'ghost' players
        """
        pass


class Table:
    """A container for:
    The deck being used.
    The 3-8 tiles viewable on the table.
    The "player pieces" indicating each player's selections.
    """
    def __init__(self, deck, num_player_pieces):
        self.deck = deck

        self.num_player_pieces = num_player_pieces
        self.empty_tuple = (None, ) * self.num_player_pieces

        self.current_market = self.empty_tuple
        self.current_player_pieces = self.empty_tuple
        self.future_market = self.empty_tuple
        self.future_player_pieces = self.empty_tuple

    def __str__(self):
        playstate = ""
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"


    def advance_tiles(self, last_round = 0):
        """ Advances the board state for the next round.

        'Slides' the future tiles and player markers into the current piece position,
        Then Deals 4 new tiles.
        """
        #Moves future pieces to the current place
        self.current_market = self.future_market
        self.current_player_pieces = self.future_player_pieces

        # Replaces the future market with new tiles
        self.future_player_pieces = self.empty_tuple
        if last_round: #On the last round, don't draw new tiles (would probably lead to an empty-deck error)
            self.future_market = self.empty_tuple
            return
        new_market = [self.deck.deal_tile() for n in range(self.num_player_pieces)]
        new_market.sort(key=lambda x: x.value) # sort the tiles by their value
        self.future_market = tuple(new_market)
        return