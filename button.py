'''
This file contains all of the logic pertaining to the various buttons that this
demo requires
'''

# pylint: disable= E1101

import pygame
from display import YELLOW, GREY

pygame.init()

class Button:
    '''
    This class allows for the user to make multiple buttons that all have the same
    underlying functionality
    '''

    def __init__(self, x_pos, y_pos, width, height, colour, not_colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = colour
        self.not_colour = not_colour
        self.width = width
        self.height = height
        self.box = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.pressed = False

    def draw_button(self, screen):
        '''
        Method to draw the buttons to the screen
        '''
        pygame.draw.rect(screen, self.colour, (self.x_pos, self.y_pos, self.width, self.height))

    def handle_event(self, event):
        '''
        This method will only do something if the user clicks on the input box
        Input:
            event (event obj) - The pygame event (ie. button click, key press, etc.)
        Output:
            A boolean value denoting that the button has been pressed
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.collidepoint(event.pos):
                self.pressed = not self.pressed
            else:
                self.pressed = False

            self.colour = YELLOW if self.pressed else GREY
