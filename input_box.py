'''
This file outlines the class that can be used to setup input boxes for our demo
'''

# pylint: disable= E1101, R0913, R1710

import pygame

pygame.init()
YELLOW = pygame.Color("#fcdb38")
GREY = pygame.Color("#D3D3D3")
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 32)

class InputBox:
    '''
    This class allows for the user to make input boxes in an object-oriented manner
    '''

    def __init__(self, x_pos, y_pos, width, height, text=''):
        self.box = pygame.Rect(x_pos, y_pos, width, height)
        self.colour = GREY
        self.text = text
        self.text_surface = FONT.render(text, True, self.colour)
        self.active = False

    def handle_event(self, event):
        '''
        This method will only do something if the user clicks on the input box
        Input:
            event (event obj) - The pygame event (ie. button click, key press, etc.)
        Output:
            The string the user entered if, otherwise None
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            self.colour = YELLOW if self.active else GREY

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.text_surface = FONT.render(self.text, True, BLACK)

    def update(self):
        '''
        Method to resize the box if the text is too long
        '''
        width = 50
        if self.text_surface.get_width() > 45:
            width = min(200, self.text_surface.get_width()+10)
        self.box.w = width

    def draw(self, screen):
        '''
        Draw the textbox to the given screen
        Input:
            screen (screen obj) - The screen that pygame is using for the main instance of
                                  the demo
        Output:
            None
        '''
        screen.blit(self.text_surface, (self.box.x+5, self.box.y+5))
        pygame.draw.rect(screen, self.colour, self.box, 2)
