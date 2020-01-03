import Board
import Tiles


class Game:

    pass

class Players:
    """Container for:
    Player's name
    Player's board
    Player's chosen tile(s)"""
    #The class keeps a dictionary of all players to their boards.
    player_boards = {}
    player_tiles = {}

    def __init__(self, player_name, board = None):
        if player_name in self.player_boards:
            print("That player already exists. Choose a different name.")
            return

        #You can assign a player a board. Otherwise, they are given a new one
        if board:
            assert isinstance(board, Board.Board), 'Provided boards must be an instance of the Board class'
            self.board = board
        else:
            self.board = Board.Board()

        self.player_boards[player_name] = board

    def __iter__(self):
        """Iterate through the players in player order
        If no tiles selected, do random print a message "WARNING, no player order"
        """
        pass

    def get_player_board(self, player_name):
        return self.player_boards[player_name]

    def get_player_tile(self, player_name):
        return self.player_tiles[player_name]

    def give_player_tile(self, player_name, tile):
        if isinstance(tile, Tiles.Tile):
            self.player_tiles[player_name] = tile
        else:
            print("Player tiles must be instances of the Tile class.")

    def new_game(self):
        self.player_boards, self.player_tiles = {}, {}





class Table:
    """A container for:
    The deck class being used.
    The 4-8 tiles viewable on the table.
    The primary draw methods for displaying the game
    The buttons that a player clicks to rotate the tile

    The game board should be pretty static. You only need to refresh when
    A tile is placed, rotated, or a choice is made.
    """

    pass

# TODO A "turn" is as follows: 1. Player places a tile, 2. Player chooses a tile