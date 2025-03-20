from dataclasses import field
from time import time_ns

import Game
import random

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

        print("game is over")
        print(self)

    def __str__(self):

        playstate = f"\nCURRENT STATE OF THE PLAY:\n"
        for key, value in self.__dict__.items():
            playstate += f"\n{key}: {value}"
        return playstate + "\n"

    def gather_starting_information(self):
        #self.player_count = self._get_input_integer("How many players? (2-4)", 2, 4)
        self.message = "How many players?"
        player_count = self._get_input_integer("(2-4)", 2, 4)
        self.message = "How should I call you?"
        player_names=[]
        for player in range(player_count):
            player_names.append(self._get_input_string(f"Player {player + 1}:", default=f"Player {player + 1}"))
        self.message = "Enable optional scoring?"
        self._get_input_string("(Not yet implemented)")
        self.game = Game.Game(player_names)
        return

    def begin_playing(self):

        print("Ok, let's pick a random player to start...")
        first_player = self.game.get_current_player()
        input(f"{first_player.get_handle()} gets to go first! Press any key to begin.")

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
        current_player = self.game.get_current_player()
        if not current_player:
            return #If there is no player, skip the turn
            #(In a 3-player round, 1 of the 4 turns each round is skipped)


        #retrieve a duplicate of the game state from the Game class
        #make changes to that duplicate


        #A turn is placing the current tile, choosing a new one, then checking to see if it's done.

        self.message = f"Ok {current_player.get_handle()}, where/how would you like to place {self.game.get_current_tile()} in your grid?"
        self.place_current_tile(current_player)

        self.message = f"Ok {current_player.get_handle()}, choose the tile you would like from the Future Market"
        self.choose_new_tile(current_player)

        self.message = "Type 'U' to undo the turn, or press ENTER to end the current turn."
        redo_turn = self._get_input_string(
            "(U, 'ENTER')",
            1, ["u"], "")
        if redo_turn == "U":
            self.game.revert_to_save_point()
            self.error_message = "Resetting to the start of your turn..."
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
            return
        self._get_tile_placement(current_player)
        # if current tile is None, (probably because it's the first round), skip this step
        # ideally this logic would be offloaded to the Game class, but oh well
        return

    def choose_new_tile(self, current_player):
        new_tiles = self.game.table.get_future_market()
        if not new_tiles[0]:
            return 0

        selection = self._get_input_integer(
            f"(1, 2, 3, or 4)",
            1, 4)
        allowed = self.game.choose_new_tile(selection)
        if not allowed:
            self.error_message = "That tile has already been chosen. Try again"
            self.choose_new_tile(current_player)
        else:
            return 1


    def display_game_state(self):
        game_visualization = "\n"
        # Show the round, turn, and player's name
        if not self.setup: # Only show this info if the setup is complete
            current_player = self.game.get_current_player()
            game_visualization += "{0:^80}".format(f"{current_player.get_handle()}'s Turn "
                                                   f"(Round {self.game.current_round + 1}, "
                                                   f"Turn {self.game.current_tile_id + 1})")
            # Add player's board
            game_visualization += str(current_player.board)[2:]

            #Prep for showing the market row
            #Build the current tile in its proper rotational order
            #todo

            #Build a list of the current market and player turns
            current_tiles = list(self.game.table.get_current_market())
            current_tiles.insert(0, "Current Market")

            #Build a list of the future market and player selections
            future_tiles = list(self.game.table.get_future_market())
            future_tiles.insert(0, "Future Market")
            #todo player selections


            for line_number in range(5): # Zip the market row together
                l = "\n"
                l += "{0:^20}".format(f"Number {line_number}")
        # Shows the current tile in its proper rotational order
                pass

                #Add Current Market to string
                l += "{0:<30}".format(str(current_tiles[line_number]))

                #Add Future Market to string
                if line_number == 0: # Don't include line number for header row
                    l += "{0:<30}".format(f"{future_tiles[line_number]}")
                else:
                    l += "{0:<30}".format(f"{line_number}.) {future_tiles[line_number]}")

                game_visualization += l

        # Shows the message fields
        if self.error_message != "":
            game_visualization += f"\nError: {self.error_message}"
            self.error_message = ""
        game_visualization += f"\n{self.message}"

        print(game_visualization)
        return

    def _get_input_integer(self, prompt, min_value=float("-inf"), max_value=float("inf")):
        """Prompts user for an integer input, enforcing minimum and maximum values"""
        while True:
            self.display_game_state()
            try:
                num = int(input(prompt+" "))
                if min_value <= num <= max_value:
                    return num
                else:
                    self.error_message = "That number is too big or small."
                    continue
            except ValueError:
                self.error_message = "Invalid input!"


    def _get_input_string(self, prompt, max_length=10, permitted_strings=[], default=None):
        """"All strings are uppercased using .upper. This isn't elegent
        """
        permitted_strings = [i.upper() for i in permitted_strings]
        while True:
            self.display_game_state()
            try:
                usr_input = input(prompt+" ")
                if usr_input == "" and default is not None:
                        return default #returns the default parameter, only if it's specified.
                assert len(usr_input) <= max_length
                if permitted_strings:
                    if usr_input.upper() in permitted_strings:
                        return usr_input.upper()
                    else:
                        self.message = "I don't understand that response."
                else:
                    return usr_input
            except AssertionError:
                self.error_message = f"Input cannot be longer than {max_length} characters"

    def _get_tile_placement(self, current_player):
        while True:
            self.display_game_state()
            input(f"Coordinates: ")
            return


if __name__ == "__main__":
    Play()