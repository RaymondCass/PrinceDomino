from dataclasses import field
from time import time_ns

import Game
import traceback
import Tiles

class Play:
    """This class defines a terminal interface for playing PrinceDomino
    When run, it prompts users through a game, accepting all inputs
    and printing out command-line renditions of the game.

    It interfaces with the Game class, which handles all game logic.

    """
    def __init__(self):
        print("Welcome to PrinceDomino!\nI have a few quick questions, then you can play!")
        self.game = None
        self.message = ""
        self.error_message = ""

        self.setup = True
        self.gather_starting_information()
        print("\nOk, we're ready to play!")
        self.setup = False
        self.begin_playing()

        self.display_scores()


    def __str__(self):

        playstate = f"\nCURRENT STATE OF THE PLAY:\n"
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"


    def gather_starting_information(self):
        deck_type, center_kingdom, full_kingdom, grid_size = 1, 0, 0, 5

        self.message = "How many players?"
        player_count = self._ask_for_input_integer("(2-4)", 2, 4)
        self.message = "How should I call you?"
        player_names=[]
        for player in range(player_count):
            player_names.append(self._ask_for_input_string(f"Player {player + 1}:", default=f"Player {player + 1}"))
        self.message = "Would you like to see the additional scoring options? (These are not enabled by default)"

        yes_no_to_bool = {"y": True, "Y": True, "n": False, "N": False}
        opt_scoring = self._ask_for_input_string("(Y/N)", permitted_strings=["y","Y","n","N"], default = "N")
        if yes_no_to_bool[opt_scoring]:
            self.message = "Enable center kingdom? (Score 10 points if your castle/'wild' is in the center of your board)"
            center_kingdom = self._ask_for_input_string("(Y/N)", permitted_strings=["y", "Y", "n", "N"], default="No")
            center_kingdom = yes_no_to_bool[center_kingdom]

            self.message = f"Enable full kingdom? (Score 5 points if your {grid_size}x{grid_size} grid is completely filled in)"
            full_kingdom = self._ask_for_input_string("(Y/N)", permitted_strings=["y","Y","n","N"], default = "No")
            full_kingdom = yes_no_to_bool[full_kingdom]

        self.game = Game.Game(player_names,
                              center_kingdom = center_kingdom,
                              full_kingdom = full_kingdom,
                              grid_size = 5)
        return

    def begin_playing(self):

        print("Ok, let's pick a random player to start...")
        first_player = self.game.get_current_player()
        input(f"{first_player.handle} gets to go first! Press any key to begin.")

        #keep taking turns until the game is over
        game_is_not_over = 1
        while game_is_not_over:
            self.take_a_turn()
            game_is_not_over = self.game.next_turn()
        return

        # if the end of the turn order has been reached, need to do upkeep.
            #Upkeep: discard all unchosen dominos from the current round
            #Upkeep: move the "future round" dominos to the current round
            #Recalculates turn order based on what everybody selected
            #deals out 4 new "future round" dominos
        # then scoring happens

    def take_a_turn(self):
        #todo once 3-player rules are correct, I should be able to remove
        # a lot of the checks for None players
        current_player = self.game.get_current_player()
        if not current_player:
            return #If there is no player, skip the turn
            #(In a 3-player round, 1 of the 4 turns each round is skipped)


        #retrieve a duplicate of the game state from the Game class
        #make changes to that duplicate


        #A turn is placing the current tile, choosing a new one, then checking to see if it's done.

        self.message = f"Ok {current_player.handle}, where/how would you like to place {self.game.get_current_tile()} in your grid?"
        self.place_current_tile(current_player)

        self.message = f"Ok {current_player.handle}, choose the tile you would like from the Future Market"
        self.choose_new_tile(current_player)

        self.message = "Type 'U' to undo the turn, or press ENTER to end the current turn."
        redo_turn = self._ask_for_input_string(
            "(U, 'ENTER')",
            1, ["u", "U"], "")
        if redo_turn == "U":
            self.game.revert_to_save_point()
            self.error_message += "\nResetting to the start of your turn..."
            self.take_a_turn()
        elif redo_turn == "":
            return
        else:
            self.message = "You pressed something other than enter, try again."
        return

    def place_current_tile(self, current_player):
        """Options when placing tile:
        To place, specify X, Y coordinate of tile. Format?
        To rotate, press "R" to rotate clockwise
        To pass, Type "P or "Pass" (only if no move available)
        """
        current_tile = self.game.get_current_tile()
        if not current_tile:
            # if current tile is None, (probably because it's the first round), skip this step
            # ideally this logic would be offloaded to the Game class, but oh well
            return

        coord = self._ask_for_tile_placement(current_player)

        # Rotation Handling
        if coord == "R":
            current_tile.rotate()
            self.error_message += "\nTile Rotated"
            #rotate
            self.place_current_tile(current_player)
            return 1

        # Pass Handling
        if coord == "P":
            self.error_message += "\nPassing not yet implemented... but fine, lol"
            #todo implement passing, don't just allow it whenever
            return 1
            self.place_current_tile(current_player)
            return 1

        allowed, error = self.game.try_to_place_tile(coord)
        self.error_message += f"{error}"
        if allowed:
            return 1
        else:
            self.place_current_tile(current_player)

    def choose_new_tile(self, current_player):
        """Prompts the player for a tile choice.
        Will continually prompt until a valid input is given.

        Then, passes the input to the self.Game.
        If the move is invalid, tries again recursively"""

        new_tiles = self.game.table.future_market
        if not new_tiles[0]:
            return 0

        selection = self._ask_for_input_integer(
            f"(1, 2, 3, or 4)",
            1, 4)
        allowed = self.game.choose_new_tile(selection)
        if not allowed:
            self.error_message += "\nOops. That tile has already been chosen. Try again"
            self.choose_new_tile(current_player)
        else:
            return 1


    def _ask_for_input_integer(self, prompt, min_value=float("-inf"), max_value=float("inf")):
        """Prompts user for an integer input, enforcing minimum and maximum values"""
        while True:
            self.display_game_state()
            try:
                num = int(input(prompt+" "))
                if min_value <= num <= max_value:
                    return num
                else:
                    self.error_message += "\nError: That number is too big or small."
                    continue
            except ValueError:
                self.error_message += "\nError: Invalid input!"

    def _ask_for_input_string(self, prompt, max_length=10, permitted_strings=[], default=None):
        """"All strings are uppercased using .upper. This isn't elegant
        """
        permitted_strings = [i.upper() for i in permitted_strings]
        while True:
            self.display_game_state()
            try:
                usr_input = input(prompt+" ")
                if (usr_input == "") and (default is not None):
                        return default #returns the default parameter, only if it's specified.
                assert len(usr_input) <= max_length
                if permitted_strings:
                    if usr_input.upper() in permitted_strings:
                        return usr_input.upper()
                    else:
                        self.error_message += "\nI don't understand that response."
                else:
                    return usr_input
            except AssertionError:
                self.error_message += f"\nError: Input cannot be longer than {max_length} characters"

    def _ask_for_tile_placement(self, current_player):

        while True:
            self.display_game_state()
            try:
                coord = input(f"Coordinates: ")
                assert len(coord) <= 2

                # a little bit of input cleansing
                coord = coord.upper()
                drooc = coord[::-1]
                if coord in current_player.board.valid_coordinates:
                    return coord
                elif drooc in current_player.board.valid_coordinates:
                    return drooc

                elif coord == "R" or coord == "P":
                    return coord
                else:
                    self.error_message += f"\nError: Your input '{coord}' is not a valid coordinate"
                    continue
            except Exception:
                traceback.print_exc()
                self.error_message += "\nError: Invalid input."


    def display_game_state(self):
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
            future_pieces = list(self.game.table.get_future_player_pieces())
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
        if self.error_message != "":
            game_visualization += f"{self.error_message}"
            self.error_message = ""
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
        if debug:
            print(self)
        game_visualization = "\n\n\ngame is over"
        scores = self.game.score_boards()
        winner = max(scores, key=lambda score: scores[score][0])
        game_visualization += "\nHere are the scores:"


        for player in scores:
            player_score = scores[player]

            breakdown = f"{player.handle}'s Total Score = {player_score[0]}\nBreakdown:"
            for category in player_score[1]:
                breakdown += f"\n   {category}: {player_score[1][category]}"
            game_visualization += f"\n\n{breakdown}"
        game_visualization += f"\n\n{winner.handle} is the winner with a score of {scores[winner][0]}"


        print(game_visualization)

        return


if __name__ == "__main__":
    Play()