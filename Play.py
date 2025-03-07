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

        #self.player_count = 0
        #self.player_names = {}

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
        first_player = self.game.get_current_player().get_handle()
        input(f"{first_player} gets to go first! Press any key to begin.")

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

        #
        #retrieve a duplicate of the game state from the Game class
        #make changes to that duplicate

        #A turn is placing the current tile, choosing a new one, then checking to see if it's done.
        self.place_current_tile()
        self.choose_new_tile()


        #input("Press ENTER to confirm, or U to undo the turn. (U not implemented)")
        # todo undo handling
        # if CONFIRM, kill the old game state, replace with the new one, then return
        # if UNDO, discard the new game state, and start at the top of this function.
        return



    def place_current_tile(self):
        """Options when placing tile:
        To place, specify X, Y coordinate of tile. Format?
        To rotate, press "R" to rotate clockwise
        To pass, Type "P or "Pass" (only if no move available)
        """
        current_tile = self.game.get_current_tile()
        if not current_tile:
            return
        current_player = self.game.get_current_player()
        if current_player:
            input(f"Ok {current_player.get_handle()}, where/how would you like to place your tile in your grid?")
        # if current tile is None, (probably because it's the first round), skip this step
        pass

    def choose_new_tile(self):
        current_player = self.game.get_current_player()
        if not current_player:
            return
        new_tiles = self.game.get_future_tiles()
        if new_tiles[0] != None:
            self._get_input_integer(f"Ok {current_player.get_handle()}, choose a tile (1, 2, 3, or 4):",
                                1, 4)
        # if future tile is None (probably because it's the final round), skip it.
        pass

    #maybe a "turn" function. With optional parameters for first/last, which activated/deactivates
    #choose new tile or place current tile respectively. And also is a holder for the current state
    #of the turn, but has the option to reset everything before committing it.

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
        """"permitted characters is not case-sensitive for single-letter characters
        """
        permitted_strings = [i.upper() for i in permitted_strings]
        while True:
            try:
                usr_input = input(prompt+" ")
                if usr_input == "" and default is not None:
                        return default
                assert len(usr_input) <= max_length
                if permitted_strings:
                    if usr_input.upper() in permitted_strings:
                        return usr_input
                    else:
                        print("I don't understand that response.")
                else:
                    return usr_input
            except AssertionError:
                print(f"Input cannot be longer than {max_length} characters")



if __name__ == "__main__":
    Play()