# Libraries
import pygame
import time

# Local modules
import classes.menu as menu_classes
from functions.loops.create_account_loop import run as create_account
from functions.loops.log_in_loop import run as log_in

# Constants
from classes.global_data import constants_structure
constants = constants_structure()

# Set up enviroment

# Used pygame docs: https://www.pygame.org/docs/
pygame.init()
screen = pygame.display.set_mode(constants.DEFAULT_SCREEN_SIZE)
pygame.display.set_caption('Dungeon Game')


defaultCharacterLog = {"mouse_down": False,
                "mouse_first_click": False
                }





# MENU OBJECTS
menu_buttons = [
    menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5), 
                        size=(600, 200), 
                        text="Log-In", 
                        response_function=log_in,
                        font=constants.TITLE_FONT),
    menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*4), 
                        size=(600, 200), 
                        text="Create Account", 
                        response_function=create_account,
                        font=constants.TITLE_FONT)
]


loop = True

# The menu where a user chooses between making a new account or logging into an existing one
while loop:
    tick_start = time.time()
    
    # FRAME CONSTANTS ONE
    mouse_pos = pygame.mouse.get_pos()
    
    
    # CHECK EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            
        if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
            for button in menu_buttons:
                if button.under_pointer:
                    button.response_function(screen)
                else:
                    button.selected = False
            
            
            
            
    # PROCESS
    for button in menu_buttons:
        button.update(mouse_pos)
    
    # RENDER
    screen.fill("gray")
    for button in menu_buttons:
        screen = button.draw(screen)
    
    
    # flip() draws screen to display
    pygame.display.flip()

    # Pause remainder of tick
    time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))

