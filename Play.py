from dataclasses import field
from time import time_ns

import Game
import traceback
import Tiles

class Play:
    """This class runs a full game of PrinceDomino in the command line.
    It prompts users for input, parses and validates those inputs,
    and passes them to the Game class in the expected order.

    It also contains the main game loop, a while loop that defines what a turn is.
    This loop continues until the game is over, at which point display_scores is called
    and the game ends.

    This class is closely related to the Game class, and the game logic is distributed
    between the two of them. Eventually, this class will be deprecated once a new UI
    is created, and the game loop is moved into the Game class itself.
    """

    def __init__(self):
        self.message = ""
        # self.message is displayed just before any prompt. The message remains the same until a new message is given
        self.temp_messages = ["Welcome to PrinceDomino!","I have a few quick questions, then you can play!"]
        # self.temp_messages are displayed just before self.message, and clear after they are seen.

        self.setup = True
        self.game = self.gather_starting_information()
        self.setup = False

        self.play_game()

        self.display_scores(debug=True)

    def __str__(self):
        playstate = f"\nCURRENT STATE OF PLAY:\n"
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate


    def gather_starting_information(self):
        """Prompts the player for the information needed to initialize a game of PrinceDomino.
        Prompts for: player count and names, end game scoring options
        Returns a Game object created using those parameters.
        """

        #Default values
        deck_type, center_kingdom, full_kingdom, grid_size = 1, 0, 0, 5
        yes_no_to_bool = {"y": True, "Y": True, "n": False, "N": False}

        self.message = "How many players?"
        player_count = self._ask_for_input_integer("(2-4)", 2, 4)

        self.message = "How should I call you?"
        player_names=[]
        for player in range(player_count):
            player_names.append(self._ask_for_input_string(f"Player {player + 1}:", default=f"Player {player + 1}"))

        self.message = "Would you like to see the additional scoring options? (By default, not enabled)"
        opt_scoring = self._ask_for_input_string("(Y/N)", permitted_strings=["y","Y","n","N"], default = "N")
        if yes_no_to_bool[opt_scoring]:

            self.message = "Enable center kingdom? (Score 10 points if your castle/'wild' is in the center of your board)"
            center_kingdom = self._ask_for_input_string("(Y/N)", permitted_strings=["y", "Y", "n", "N"], default="No")
            center_kingdom = yes_no_to_bool[center_kingdom]

            self.message = f"Enable full kingdom? (Score 5 points if your {grid_size}x{grid_size} grid is completely filled in)"
            full_kingdom = self._ask_for_input_string("(Y/N)", permitted_strings=["y","Y","n","N"], default = "No")
            full_kingdom = yes_no_to_bool[full_kingdom]

        return Game.Game(player_names, center_kingdom = center_kingdom, full_kingdom = full_kingdom, grid_size = grid_size)

    def play_game(self):
        """This is the main game loop.
        Until the game is over, take a turn, then advance to the next turn.
        Returns 1 when the game is over.
        """
        first_player = self.game.get_current_player()
        input(f"{first_player.handle} has been randomly chosen to go first! Press any key to begin.")

        #keep taking turns until the game is over
        game_is_not_over = 1
        while game_is_not_over:
            self.take_a_turn()
            game_is_not_over = self.game.next_turn()
        return 1

    def take_a_turn(self):
        """In a turn, the current player places the current tile, chooses a new one, and then has the option to undo."""
        current_player = self.game.get_current_player()

        self.message = f"Ok {current_player.handle}, where/how would you like to place {self.game.get_current_tile()} in your grid?"
        self.place_current_tile(current_player)

        self.message = f"Ok {current_player.handle}, choose the tile you would like from the Future Market"
        self.choose_new_tile(current_player)

        self.message = "Type 'U' to undo the turn, or press ENTER to end the current turn."
        redo_turn = self._ask_for_input_string("(U, 'ENTER')",1, ["u", "U"], "")
        if redo_turn in ["U","u"]:
            # If the player decides to undo, revert the game state and start from the top of this method.
            self.game.revert_to_save_point()
            self.temp_messages.append("Resetting to the start of your turn...")
            self.take_a_turn()
        return 1

    def place_current_tile(self, current_player):
        """Prompts the current player on the tile placement part of their turn.
        Then passes the player input to game.try_to_place_tile.

        This method repeats until the player successfully places the tile (or passes).
        """
        current_tile = self.game.get_current_tile()
        if not current_tile:
            return # if current tile is None, (probably because it's the first round), skip this step

        player_input = self._ask_for_tile_placement(current_player)
        move_allowed, error = self.game.try_to_place_tile(player_input)
        if error:
            self.temp_messages.append(error)

        if move_allowed:
            return 1
        else:
            self.place_current_tile(current_player)

    def choose_new_tile(self, current_player):
        """Prompts the current player to choose a tile from the future market.
        Then passes the player input to self.game.choose_new_tile

        This method repeats until the player successfully selects a tile.
        """
        new_tiles = self.game.table.future_market
        if not new_tiles[0]:
            return 0 #on the last turn, skip this step

        # Creates an input prompt in the form of (1, 2, 3, 4 ..., or n), based on the number of tiles available
        prompt = [str(i) for i in range(1, self.game.num_player_pieces + 1)]
        prompt = f"({', '.join(prompt[:-1]) + ', or ' + prompt[-1] if self.game.num_player_pieces > 1 else prompt[0]})"

        selection = self._ask_for_input_integer(prompt,1, self.game.num_player_pieces)
        move_allowed = self.game.try_to_choose_new_tile(selection)

        if not move_allowed:
            self.temp_messages.append("Oops. That tile has already been chosen. Try again")
            self.choose_new_tile(current_player)
        else:
            return 1


    def _ask_for_input_integer(self, prompt, min_value=float("-inf"), max_value=float("inf")):
        """Helper method that generates a prompt for an integer input.
        The user is presented with prompt, then must input an integer.
        Minimum and Maximum values are enforced.
        """
        while True:
            self.display_game_state()
            try:
                num = int(input(prompt+" "))
                if min_value <= num <= max_value:
                    return num
                else:
                    self.temp_messages.append("Error: That number is too big or small.")
                    continue
            except ValueError:
                self.temp_messages.append("Error: Invalid input!")

    def _ask_for_input_string(self, prompt, max_length=10, permitted_strings=[], default=None):
        """Helper method that generates a prompt for a string input.
        The user is presented with prompt, then must input an integer.
        Maximum length is enforced, and is 10 characters by default.

        If permitted_strings is specified, the user's response must be one of those strings.

        If default is specified, it is returned if the user does not enter anything.
        (The default value does not need to be included in permitted_strings)
        """
        while True:
            self.display_game_state()
            try:
                usr_input = input(prompt+" ")
                if (usr_input == "") and (default is not None):
                        return default # returns the default parameter, only if it's specified.

                assert len(usr_input) <= max_length
                if permitted_strings:
                    if usr_input in permitted_strings:
                        return usr_input
                    else:
                        self.temp_messages.append("I don't understand that response.")

                else:
                    return usr_input
            except AssertionError:
                self.temp_messages.append(f"Error: Input cannot be longer than {max_length} characters")

    def _ask_for_tile_placement(self, current_player):
        """Prompts player for input during the tile placement phase of their turn.
        Returns the player's input (capitalized and reordered). Inputs are not case-sensitive.

        Valid inputs are as follows:
        A coordinate on their board, as specified by board.valid_coordinates. E.g. A5, 2b
        'R' or 'P' for rotate or pass.
        """

        while True:
            self.display_game_state()
            try:
                coord = input(f"Coordinates: ")
                assert len(coord) <= 2

                # a little bit of input cleansing, to allow for more leniency.
                coord = coord.upper()
                drooc = coord[::-1]

                if coord in current_player.board.valid_coordinates:
                    return coord
                elif drooc in current_player.board.valid_coordinates:
                    return drooc

                elif coord == "R" or coord == "P":
                    return coord
                else:
                    self.temp_messages.append(f"Error: '{coord}' is not a valid coordinate or action")
                    continue
            except Exception:
                self.temp_messages.append(traceback.print_exc())
                self.temp_messages.append("Error: Invalid input.")


    def display_game_state(self):
        """This method constructs a string that shows all the information a player needs to take their turn.
        It is called whenever a player is asked to provide input, and provides the context needed to make that decision.

        It displays self.message and self.temp_messages (then clears temp_messages).

        When the game is ongoing, it shows the current player's board.
        Underneath that, it shows the current tile being placed, the current turn order, and the future available tiles.
        """

        game_visualization = "\n"
        # Show the round, turn, and player's name
        if not self.setup: # Only show this info if the setup is complete
            current_player = self.game.get_current_player()
            game_visualization += "{0:^80}".format(f"{current_player.handle}'s Turn "
                                                   f"(Round {self.game.current_round }/{self.game.number_of_rounds}, "
                                                   f"Turn {self.game.current_turn + 1})")
            # Add player's board
            game_visualization += str(current_player.board)[2:]

            #Prep for showing the market row
            #Build the current tile in its proper rotational order
            current_tile = self._tile_string(self.game.get_current_tile())

            #Build a list of the current market and player turns
            current_market = list(self.game.table.current_market)
            current_market.insert(0, "Current Market")
            current_players = list(self.game.table.current_player_pieces)
            current_players.insert(0, None)

            #Build a list of the future market and player selections
            future_market = list(self.game.table.future_market)
            future_market.insert(0, "Future Market")
            future_pieces = list(self.game.table.future_player_pieces)
            future_pieces.insert(0, None)

            for line_number in range(len(future_market)): # Zip the market row together
                l = "\n"
                l += current_tile[line_number]

                #Add Current Market to string
                cm_player = current_players[line_number]
                if line_number == 0:
                    l += "{0:<30}".format(f"{current_market[line_number]}")
                else:
                    if not cm_player:
                        cm_string = ""
                    elif self.game.current_turn + 1 == line_number:
                        cm_string = f"   {str(cm_player.handle)}'s turn"
                    elif self.game.current_turn + 1 > line_number:
                        cm_string = ""
                    else:
                        cm_string = f"{current_market[line_number]} ({cm_player.handle})"
                    l += "{0:<30}".format(cm_string)

                #Add Future Market to string
                fm_player = future_pieces[line_number]
                if not fm_player:
                    fm_player = ""
                else:
                    fm_player = f" ({fm_player.handle})"
                #Add line numbers to future markets
                if line_number == 0: # Don't include line number for header row
                    l += "{0:<30}".format(f"{future_market[line_number]}")
                else:
                    l += "{0:<30}".format(f"{line_number}.) {future_market[line_number]}{fm_player}")

                game_visualization += l

        # Shows the message fields
        if self.temp_messages:
            game_visualization += "".join(["\n" + message for message in self.temp_messages])
            self.temp_messages = []
        game_visualization += f"\n{self.message}"

        print(game_visualization)
        return

    def _tile_string(self, tile):
        """Helper function for display_game_state.

        Returns a list of 5 len(20) strings.
        string depiction of the Tile object,
        As a list of 5 len(20) strings."""

        if  isinstance(tile, Tiles.Tile):
            s1, s2, direction = tile.get_square1(), tile.get_square2(), tile.get_direction()
            s1, s2 = "*"+str(s1), str(s2)
            fs1, fs2 = "{:^20}".format(s1), "{:^20}".format(s2)
            e, d = "{:^20}".format(""), "{:^20}".format("-------")
            if direction == "right":
                tile_str = [e,e,"{:^20}".format(f"{s1}|{s2}"),e,e]
            elif direction == "left":
                tile_str = [e,e,"{:^20}".format(f"{s2}|{s1}"),e,e]
            elif direction == "up":
                tile_str = [e,fs2,d,fs1,e]
            elif direction == "down":
                tile_str = [e,fs1,d,fs2,e]
            return tile_str
        else:
            return ["{0:^20}".format("") for row in range(5)]

    def display_scores(self, debug = False):
        """Prints out the scorecard at the end of the game.
        If debug is set to true, also prints the Play object.
        """

        if debug:
            print(self)
        scorecard = "\n\n\ngame is over"
        scores = self.game.score_boards()
        winner = max(scores, key=lambda score: scores[score][0])
        scorecard += "\nHere are the scores:"

        for player in scores:
            player_score = scores[player]
            breakdown = f"{player.handle}'s Total Score = {player_score[0]}\nBreakdown:"
            for category in player_score[1]:
                breakdown += f"\n   {category}: {player_score[1][category]}"
            scorecard += f"\n\n{breakdown}"

        scorecard += f"\n\n{winner.handle} is the winner with a score of {scores[winner][0]}"
        print(scorecard)
        return 1



if __name__ == "__main__":
    Play()