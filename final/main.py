# FIRST WINDOW AND MAIN GAME FILE

# Libraries
import pygame
import time

# Open window
pygame.init()
screen = pygame.display.set_mode((1000, 720))
pygame.display.set_caption('Dungeon Game')

# Local modules
import classes.menu as menu_classes
from functions.loops.create_account_loop import run as create_account
from functions.loops.log_in_loop import run as log_in
# Constants
from classes.global_data import constants_structure
constants = constants_structure()

# Buttons
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
while loop:
    tick_start = time.time()
    
    # FRAME CONSTANTS ONE
    mouse_pos = pygame.mouse.get_pos()
    
    # CHECK EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit program
            print("Closing program, goodbye!")
            quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
            for button in menu_buttons:
                if button.under_pointer:
                    button.response_function(screen) # Run button functions if pressed
                else:
                    button.selected = False
    
    # PROCESS
    for button in menu_buttons:
        button.update(mouse_pos)
    
    # RENDER
    screen.fill("gray")
    
    # Draw buttons
    for button in menu_buttons:
        screen = button.draw(screen)
    
    pygame.display.flip()

    # Wait for remainder of tick
    time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
