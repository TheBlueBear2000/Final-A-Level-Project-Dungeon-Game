def run(screen, key_bindings):
    import pygame
    import time
    
    import classes.menu as menu_classes
    
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    
    # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
    temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
    temp_surface.fill((100,100,100,100))
    screen.blit(temp_surface, [0,0])
    
    # Buttons
    menu_buttons = [
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*3), 
                            size=(600, 100), 
                            text="Save and Quit", 
                            font=constants.TITLE_FONT),
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*5), 
                            size=(600, 100), 
                            text="Back",
                            font=constants.NORMAL_FONT)
    ]
    
    keysPressed = []
    loop = True
    while loop:
        tick_start = time.time()
        mouse_pos = pygame.mouse.get_pos()
        
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: # Quit program
                print("Closing program, goodbye!")
                quit()
                
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) == "pause":
                    loop = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[1].under_pointer: # Back button
                    return True # True means the game can continue and doesn't have to quit
                
                elif menu_buttons[0].under_pointer: # Save and quit button
                    return False # False means game must save and quit
        
        # PROCESS
        for button in menu_buttons:
            button.update(mouse_pos, keysPressed)
        
        # RENDER
        
        # Draw text
        screen = draw_text("Game Paused", screen, constants.TITLE_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//3], (0,0,0), "centre", "above")
        pause_key = "P"
        screen = draw_text(f"Press {pause_key} to unpause", screen, constants.NORMAL_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//3], (0,0,0), "centre", "below")
        
        # Draw buttons
        for button in menu_buttons:
            screen = button.draw(screen, 0)
        
        pygame.display.flip()
        
        # Pause for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
    return
