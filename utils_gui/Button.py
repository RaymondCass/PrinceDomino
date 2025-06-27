import pygame

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, name="", linked_parameter = None, target = True):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.name=name
        self.linked_parameter = linked_parameter
        self.target = target

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if self.linked_parameter == self.target:
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        elif position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)

class Textbox(Button):
    def __init__(self, dimensions, pos, container, font, base_color, hovering_color, text_color=(0,0,0)):
        """Instead of an image, takes dimensions as a tuple (width, height) for the text box.
        Container should be a list containing a single. The text box will edit that string
        """
        #TODO if the text field is empty, display the "default" value

        self.container = container
        self.image = pygame.Surface(dimensions)
        self.image.fill((100, 0, 0))  # Black rectangle
        super().__init__(self.image, pos, self.container[0], font, base_color, hovering_color)
        self.selected = False

        self.text_color = text_color
        self.render_text()


    def changeColor(self, position):
        if self.selected:
            self.image.fill(self.hovering_color)
            return
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image.fill(self.hovering_color)
        else:
            self.image.fill(self.base_color)

    def set_text(self, event):
        if event.key == pygame.K_BACKSPACE:
            # get text input from 0 to -1 i.e. end.
            self.container[0] = self.container[0][:-1]
        else:
            if len(self.container[0]) <= 10:
                self.container[0] += event.unicode
        self.render_text()

    def render_text(self):
        self.text_input = self.container[0]
        self.text_rect = self.text.get_rect(midleft=(self.rect.left + 10, self.y_pos))  # Text inset from left
        self.text = self.font.render(self.text_input, True, self.text_color)

class BoardDisplay:
    def __init__(self, player, pos,  color, rows=7, cols=7):
        self.player = player
        self.image = self.draw_board()

        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rows, self.cols = rows, cols


    def update(self, screen):
        screen.blit(self.image, self.rect)

    def draw_board(self):

        board = pygame.Surface((250, 250))
        board.fill((100, 100, 100))
        return board

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def click_to_grid_position(self, position):
        xaxis = ((position[0]-self.rect.left) / (self.rect.right - self.rect.left) * self.cols) // 1
        yaxis = ((position[1]-self.rect.top) / (self.rect.bottom - self.rect.top) * self.rows) // 1
        return [f"clicked {position}, x-axis = {xaxis}, yaxis = {yaxis}"]



def get_font(size, name = None): # Returns font in the desired size
    return pygame.font.SysFont(name, size)