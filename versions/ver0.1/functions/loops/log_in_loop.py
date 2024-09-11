def run(screen):
    print("log in button pressed")
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    from functions.algorithms.log_in import do_log_in
    from classes.global_data import constants_structure
    from functions.loops.main_menu import run as main_menu
    # Constants
    constants = constants_structure()


    # MENU OBJECTS
    menu_buttons = [
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*5), 
                            size=(600, 100), 
                            text="Log-In", 
                            response_function=do_log_in,
                            font=constants.TITLE_FONT),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*3),
                            size=(600,100),
                            button_name="Password",
                            protected=True),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*2),
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
    while loop:
        tick_start = time.time()
        tickCount += 1
        
        # FRAME CONSTANTS ONE
        mouse_pos = pygame.mouse.get_pos()
        keysPressed = []
        
        # CHECK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[0].under_pointer: # Log-in button
                    
                    responce = menu_buttons[0].response_function(menu_buttons[2].content, # Username
                                                                menu_buttons[1].content)  # Password
                
                elif menu_buttons[3].under_pointer: # back button
                    return
                    
                for button in menu_buttons[1:]:
                    if button.under_pointer:
                        button.response_function()
                    else:
                        button.selected = False
                        
            if event.type == pygame.KEYDOWN:
                keysPressed.append(event.unicode)
                
        # PROCESS
        #if keysPressed != []:
            #print(keysPressed)
        for button in menu_buttons:
            button.update(mouse_pos, keysPressed)
            
            
        if responce != {}:
            if responce["returnType"] == 1:
                main_menu(screen, responce["account_details"])
                
                return # After main menu loop is finished, create account section should be skipped in exchange for going directly back to account select
            else:
                displayedError = menu_classes.displayedError(responce["returnMessage"], tickCount)
                
        
        # RENDER
        screen.fill("gray")
        for button in menu_buttons:
            screen = button.draw(screen, tickCount)
        
        if displayedError != None:
            screen = displayedError.draw(screen)
            
        content = constants.TITLE_FONT.render("Log-In", True, (0,0,0))
        screen.blit(content,((constants.DEFAULT_SCREEN_SIZE[0]-content.get_width())//2, int((constants.DEFAULT_SCREEN_SIZE[1]-200)//10*1.25)))
        
        
        # flip() draws screen to display
        pygame.display.flip()

        # Pause remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
        