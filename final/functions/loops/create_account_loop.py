def run(screen):
    print("create account button pressed")
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    from functions.algorithms.account_creation import addAccount as account_creation_check
    from classes.global_data import constants_structure
    from functions.loops.main_menu import run as main_menu
    # Constants
    constants = constants_structure()


    # Buttons
    menu_buttons = [
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*5.5), 
                            size=(600, 100), 
                            text="Create", 
                            response_function=account_creation_check,
                        font=constants.TITLE_FONT),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*4.5),
                            size=(600,100),
                            button_name="Re-enter Password",
                            protected=True),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*3.5),
                            size=(600,100),
                            button_name="Password",
                            protected=True),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*2.5),
                            size=(600,100),
                            button_name="Display Name"),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*1.5),
                            size=(600,100),
                            button_name="Username"),
        menu_classes.button(location=(10,10), 
                            size=(150, 50), 
                            text="Back")
        
    ]

    displayedError = None


    
    loop = True
    tickCount = 0
    responce = {}
    while loop: # Meny loop
        tick_start = time.time()
        tickCount += 1
        mouse_pos = pygame.mouse.get_pos()
        keysPressed = []
        
        # CHECK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit program
                print("Closing program, goodbye!")
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[0].under_pointer: # Create button
                    responce = menu_buttons[0].response_function(menu_buttons[4].content,   # Username
                                                        menu_buttons[1].content,            # Re-enter password
                                                        menu_buttons[2].content,            # Password (order is unnecessary)
                                                        menu_buttons[3].content,            # Display name
                                                        "")
                elif menu_buttons[5].under_pointer: # back button
                    return
                for button in menu_buttons[1:]: # All text inputs
                    if button.under_pointer:
                        button.response_function()
                    else:
                        button.selected = False
                        
            if event.type == pygame.KEYDOWN:
                keysPressed.append(event.unicode)
                
        # PROCESS
        for button in menu_buttons:
            button.update(mouse_pos, keysPressed)
            
        # Check responce if account has been created
        if responce != {}:
            if responce["returnType"] == 1:
                main_menu(screen, responce["account_details"])
                
                return # After main menu loop is finished, create account section should be skipped in exchange for going directly back to account select
            else:
                displayedError = menu_classes.displayedError(responce["returnMessage"], tickCount)
                
        
        # RENDER
        screen.fill("gray")
        
        # Draw buttons
        for button in menu_buttons:
            screen = button.draw(screen, tickCount)
        
        # Draw error
        if displayedError != None:
            screen = displayedError.draw(screen)
        
        # Draw title
        content = constants.TITLE_FONT.render("Create Account", True, (0,0,0))
        screen.blit(content,((constants.DEFAULT_SCREEN_SIZE[0]-content.get_width())//2, int((constants.DEFAULT_SCREEN_SIZE[1]-200)//10)))
        
        # Draw screen to actual window
        pygame.display.flip()

        # Wait for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
