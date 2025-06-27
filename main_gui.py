import pygame
import sys
from Princedomino import Game
from Princedomino.Defaults import DEFAULT_OPTIONS, DECK_TYPE
from utils_gui.Button import Button, Textbox, BoardDisplay,get_font
from utils_gui.gui_parameters import *

class PrinceDomino:
    def __init__(self):
        self.game = [Game.Game()] #todo remove this, placeholder game

        pygame.init()
        self.current_state = ["menu"] #options are "menu" "playing", or "game over"

        # CREATING CANVAS
        self.canvas = pygame.display.set_mode((1000, 800))

        # TITLE OF CANVAS
        pygame.display.set_caption("PrinceDomino")


        #initialize states
        self.main_menu = MainMenu(self.current_state, self.game)
        self.playing = GamePlay(self.current_state, self.game)
        self.game_over = GameOver(self.current_state, self.game)

        #main loop
        while True:
            if self.current_state[0] == "menu":
                self.main_menu.run()
            elif self.current_state[0] == "playing":
                self.playing.run()
            elif self.current_state[0] == "game over":
                self.game_over.run()


"""
So I want buttons for all the options.
Currently, I can manually create a button, which will hover when it presses but will not do anything.

It would be nice to tie the button to its action. Maybe I just add a parameter to the button class for
"function when clicked"?

Currently, clicking a button sends a signal to the MainMenu class, and which I need to parse with if statements
However, when I spawn the button, I already know what its behavior is going to be.

Plus, I'm planning for there to be so many buttons. I'm thinking buttons will be my main way of interacting with the game.
But I'm not sure - maybe there's a better way? A giant rectangular space that represents he board,
and clicking it just converts to a coordinate based on the position?

I think the button needs to be linked to the action. I don't want for the game loop to keep track and specifically
check what each button does. It seems to make sense to just store in the button what it does.

"""

class MainMenu:
    def __init__(self, current_state, game):
        self.game = game
        self.current_state = current_state
        self.canvas = pygame.display.get_surface()
        self.exit = False
        self.options = dict(DEFAULT_OPTIONS)
        self.options["PLAYER_NAMES"] = [[""],[""],[""],[""]]
        self.message = [""]
        self.background_color = (0, 0, 0)
        self.buttons = []
        self.init_menu_buttons()
        self.textboxes = []
        self.init_textboxes()



    def init_menu_buttons(self):
        self.play_button = Button(None, pos=(COL_TWO, ROW_FIVE), text_input="PLAY", font=get_font(60),
                                  base_color="#8abfbd", hovering_color="#309c97")

        #Center Kindom Buttons
        self.CK_enabled_button = Button(None, pos=(COL_TWO, ROW_TWO), text_input="Enabled", font=get_font(30),
                                        base_color="#8abfbd", hovering_color="#309c97",
                                        linked_parameter= self.options["CENTER_KINGDOM"], target = [True])
        self.CK_disabled_button = Button(None, pos=(COL_THREE, ROW_TWO), text_input="Disabled", font=get_font(30),
                                         base_color="#8abfbd", hovering_color="#309c97",
                                         linked_parameter= self.options["CENTER_KINGDOM"], target = [False])

        #FULL Kingdom Buttons
        self.FK_enabled_button = Button(None, pos=(COL_TWO, ROW_THREE), text_input="Enabled", font=get_font(30),
                                        base_color="#8abfbd", hovering_color="#309c97",
                                        linked_parameter= self.options["FULL_KINGDOM"], target = [True])
        self.FK_disabled_button = Button(None, pos=(COL_THREE, ROW_THREE), text_input="Disabled", font=get_font(30),
                                         base_color="#8abfbd", hovering_color="#309c97",
                                         linked_parameter= self.options["FULL_KINGDOM"], target = [False])

        #Player Count Buttons
        self.two_player_button = Button(None, pos=(COL_TWO, ROW_FOUR), text_input="TWO", font=get_font(30),
                                        base_color="#8abfbd", hovering_color="#309c97",
                                        linked_parameter= self.options["PLAYER_COUNT"], target = [2])
        self.three_player_button = Button(None, pos=(COL_THREE, ROW_FOUR), text_input="THREE", font=get_font(30),
                                          base_color="#8abfbd", hovering_color="#309c97",
                                          linked_parameter=self.options["PLAYER_COUNT"], target=[3])
        self.four_player_button = Button(None, pos=(COL_FOUR, ROW_FOUR), text_input="FOUR", font=get_font(30),
                                         base_color="#8abfbd", hovering_color="#309c97",
                                         linked_parameter=self.options["PLAYER_COUNT"], target=[4])

        self.buttons = [self.play_button,
                        self.CK_enabled_button, self.CK_disabled_button,
                        self.FK_enabled_button, self.FK_disabled_button,
                        self.two_player_button, self.three_player_button, self.four_player_button]

    def init_textboxes(self):
        # variables for textboxes. The first two specify the position,
        # the third value is the container it corresponds to
        parameters = [(COL_ONE, ROW_FIVE, self.options["PLAYER_NAMES"][0]),
                      (COL_TWO, ROW_FIVE, self.options["PLAYER_NAMES"][1]),
                      (COL_THREE, ROW_FIVE, self.options["PLAYER_NAMES"][2]),
                      (COL_FOUR, ROW_FIVE, self.options["PLAYER_NAMES"][3])]

        self.textboxes = [Textbox((150, 50), pos=(col, row-100),
                                        container=container, font=get_font(30),
                                        base_color="#8abfbd", hovering_color="#309c97")
                          for col, row, container in parameters]


    def update_display(self):
        """"""
        # Draw the persistent elements of the game
        # Buttons
        # Future and Current Market
        # Current Round info
        # Any message text

        # Get a surface for each player board

        # Blit each player board onto the canvas in the appropriate location
        # determine the location (to start, I'll just use fixed quadrants with a fixed resolution)

        # update the display
        self.canvas.fill(self.background_color)
        self.update_board_surface()
        self.update_buttons()
        self.update_textboxes()
        self.update_text_surface()
        pygame.display.flip()

    def update_text_surface(self):
        # text on screen
        font = get_font(25, "arial")
        text_color = (255, 255, 255)

        # message
        text_surface = font.render(self.message[0], True, text_color)
        self.canvas.blit(text_surface, (COL_TWO, ROW_ONE))

        #center Kingdom
        text_surface = font.render(f'Center Kingdom: {self.options["CENTER_KINGDOM"][0]}', True, text_color)
        self.canvas.blit(text_surface, (COL_ONE, ROW_TWO))

        #Full Kingdom
        text_surface = font.render(f'Full Kingdom: {self.options["FULL_KINGDOM"][0]}', True, text_color)
        self.canvas.blit(text_surface, (COL_ONE, ROW_THREE))

        #Player Count
        text_surface = font.render(f'Player Count: {self.options["PLAYER_COUNT"][0]}', True, text_color)
        self.canvas.blit(text_surface, (COL_ONE, ROW_FOUR))

    def update_buttons(self):
        for button in self.buttons:
            button.changeColor(self.MOUSE_POS)
            button.update(self.canvas)

    def update_textboxes(self):
        for textbox in self.textboxes:
            textbox.changeColor(self.MOUSE_POS)
            textbox.update(self.canvas)

    def update_board_surface(self, player=0):
        return
        rect = pygame.Rect(100, 50, 50, 100)
        board = pygame.Surface((200, 200))
        pygame.draw.rect(board, (255, 0, 0), rect, 10)

        self.canvas.blit(board, (0, 0))
        self.canvas.blit(board, (200, 200))



        return board

    def event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.exit = True
                pygame.quit()
                sys.exit()

            #click handling
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # For eah button
                # if the button is clicked,
                # if it has a linked value, set it to its target value.
                # set its linked value to its target value.
                for button in self.buttons:
                    if button.checkForInput(self.MOUSE_POS):
                        if button.linked_parameter:
                            button.linked_parameter[0] = button.target[0]

                for textbox in self.textboxes:
                    if textbox.checkForInput(self.MOUSE_POS):
                        textbox.selected = True
                    else:
                        textbox.selected = False

                if self.play_button.checkForInput(self.MOUSE_POS):
                    players = list(self.options["PLAYERS"])
                    player_count = self.options["PLAYER_COUNT"][0]
                    for number in range(player_count):
                        name = self.options["PLAYER_NAMES"][number][0].strip()
                        if name:
                            players[number] = name
                    players = players[:player_count]
                    self.message = [str(players)]

                    print(self.game)
                    self.game[0] = Game.Game(players = players,
                         deck_type = self.options["DECK_TYPE"][0],
                         center_kingdom = self.options["CENTER_KINGDOM"][0],
                         full_kingdom = self.options["FULL_KINGDOM"][0],
                         grid_size = self.options["GRID_SIZE"][0])
                    print(self.game)
                    self.current_state[0] = "playing"

                    # if self.options["new_friends"] == True:
                    #     self.current_state[0] = GAME_START
                    # else:
                    #     self.current_state[0] = GAME

            #keyboard handling
            if event.type == pygame.KEYDOWN:
                for textbox in self.textboxes:
                    if textbox.selected:
                        textbox.set_text(event)

    def run(self):
        while self.current_state[0] == "menu":
            self.MOUSE_POS = pygame.mouse.get_pos()
            self.update_display()
            self.event()




class GamePlay:
    def __init__(self, current_state, game):
        self.game = game #this is a list containing game
        self.current_state = current_state
        self.canvas = pygame.display.get_surface()
        self.exit = False
        self.message = ["hello"]
        self.background_color = (0, 0, 0)
        self.back_button = Button(None, pos=(50, 20), text_input="Menu", font=get_font(60),
                                  base_color="#8abfbd", hovering_color="#309c97")
        self.boards =[]


    def init_new_game(self):
        self.board = []
        print(self.game)
        for player in range(self.game[0].player_count):
            print(f"player number {player}")
            self.boards.append(BoardDisplay(None, (300 * (player + 1), 300), "Green"))

    def update_display(self):
        """"""
        # Draw the persistent elements of the game
        # Buttons
        # Future and Current Market
        # Current Round info
        # Any message text
        self.canvas.fill(self.background_color)

        for board in self.boards:
            board.update(self.canvas)


        self.update_text_surface()

        self.back_button.changeColor(self.MOUSE_POS)
        self.back_button.update(self.canvas)

        pygame.display.flip()

    def update_text_surface(self):
        # text on screen
        font = get_font(25, "arial")
        text_color = (255, 255, 255)

        # message
        text_surface = font.render(self.message[0], True, text_color)
        self.canvas.blit(text_surface, (COL_TWO, ROW_ONE))


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.checkForInput(self.MOUSE_POS):
                    self.current_state[0] = "menu"
                for board in self.boards:
                    if board.checkForInput(self.MOUSE_POS):
                        self.message = board.click_to_grid_position(self.MOUSE_POS)

    def run(self):
        self.init_new_game()

        while self.current_state[0] == "playing":
            self.MOUSE_POS = pygame.mouse.get_pos()
            self.update_display()
            self.event()


class GameOver:
    def __init__(self, current_state, game):
        self.current_state = current_state
        self.game = game
        self.canvas = pygame.display.get_surface()

    def run(self):
        pass

if __name__ == "__main__":
    PrinceDomino()