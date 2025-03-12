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

        self.gather_starting_information()
        print("Ok, we're ready to play!")

        self.current_round = 0
        self.final_round = 3 #calculate game length, don't hard-code.
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
        player_count = self._get_input_integer("How many players? (2-4)", 2, 4)
        print("What are your names?")
        player_names=[]
        for player in range(player_count):
            player_names.append(self._get_input_string(f"Player {player + 1}:", default=f"Player {player + 1}"))
        #for player in range(self.player_count):
        #    self.player_names[player] = self._get_input_string(f"Player {player + 1}:", default=f"Player {player + 1}")
        input("Enable optional Scoring? (Not yet implemented)")
        self.game = Game.Game(player_names)
        return

    def begin_playing(self):

        print("Ok, let's pick a random player to start.\n")
        first_player = self.game.get_current_player()
        input(f"{first_player.get_handle()} gets to go first! Press any key to begin.")

        #keep taking turns until the game is over
        game_is_not_over = 1
        while game_is_not_over:
            self.take_a_turn()
            game_is_not_over = self.game.next_turn()
            print("\n")
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
        self.place_current_tile(current_player)
        self.choose_new_tile(current_player)

        redo_turn = self._get_input_string(
            "Input 'U' to undo the turn, or press ENTER to end current turn.",
            1, ["u"], "")
        if redo_turn == "U":
            self.game.revert_to_save_point()
            self.take_a_turn()
        elif redo_turn == "":
            return
        else:
            print("You pressed something other than enter, try again.")
        # todo undo handling
        #   returning advances the turn and commits the save.
        #   or, don't return. Stay in this function and try again.
        # if CONFIRM, kill the old game state, replace with the new one, then return
        # if UNDO, discard the new game state, and start at the top of this function.
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
        input(f"Ok {current_player.get_handle()}, where/how would you like to place your tile in your grid?")
        # if current tile is None, (probably because it's the first round), skip this step
        return

    def choose_new_tile(self, current_player):


        new_tiles = self.game.get_future_tiles()

        print("Available (Future) tiles =")
        for i in range(len(new_tiles)):
            print(str(i+1) + ".) " + str(new_tiles[i]))
        selection = self._get_input_integer(
            f"Ok {current_player.get_handle()}, choose a tile (1, 2, 3, or 4):",
            1, 4)
        #todo pass selection on to the game.
        return


    def _get_input_integer(self, prompt, min_value=float("-inf"), max_value=float("inf")):
        """Prompts user for an integer input, enforcing minimum and maximum values"""
        while True:
            try:
                num = int(input(prompt+" "))
                if min_value <= num <= max_value:
                    return num
                else:
                    print("That number is too big or small.")
                    continue
            except ValueError:
                print("Invalid input!")

    def _get_input_string(self, prompt, max_length=10, permitted_strings=[], default=None):
        """"All strings are uppercased using .upper. This isn't elegent
        """
        permitted_strings = [i.upper() for i in permitted_strings]
        while True:
            try:
                usr_input = input(prompt+" ")
                if usr_input == "" and default is not None:
                        return default #returns the default parameter, only if it's specified.
                assert len(usr_input) <= max_length
                if permitted_strings:
                    if usr_input.upper() in permitted_strings:
                        return usr_input.upper()
                    else:
                        print("I don't understand that response.")
                else:
                    return usr_input
            except AssertionError:
                print(f"Input cannot be longer than {max_length} characters")



if __name__ == "__main__":
    Play()