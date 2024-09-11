def run(screen, account_details):
    print("opened savegames")
    
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    from classes.global_data import draw_text
    from classes.global_data import constants_structure
    import functions.algorithms.new_savegame
    # Constants
    constants = constants_structure()

    only_refreshing = True
    while only_refreshing: # Allows the page to be refreshed later so that the a savegame can be added to the list when it is created
        
        # Savegame buttons
        index = -1
        savegame_buttons = []
        savegame_button_size = (400, 200)
        for i, savegame in enumerate(account_details["savegames"]):
            if i%2 == 0:
                x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) - savegame_button_size[0] - 5
            else:
                x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) + 5
            savegame_buttons.append(menu_classes.savegameButton(location=( x_loc, 150 + ((len(savegame_buttons)//2) * (savegame_button_size[1] + 15)) ), 
                                                                size=savegame_button_size, 
                                                                savegame_display_details=savegame["display_details"],
                                                                game_data=[account_details["UUID"], savegame["display_details"]["id"]]))
            index = i
        
        # Calculate button position based on index
        index += 1
        if index%2 == 0:
            x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) - savegame_button_size[0] - 5
        else:
            x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) + 5
        new_savegame_location = ( x_loc, 
                                150 + ((len(savegame_buttons)//2) * (savegame_button_size[1] + 15)) )
        
        # Buttons
        menu_buttons = [
            menu_classes.button(location=(10,10), 
                                size=(150, 50), 
                                text="Back",
                                font=constants.NORMAL_FONT),
            menu_classes.button(location=new_savegame_location, 
                                size=(400, 200), 
                                text="+", 
                                response_function=functions.algorithms.new_savegame.entry_loop,
                                font=constants.TITLE_FONT)
        ]
        
        loop = True
        while loop:
            tick_start = time.time()
            mouse_pos = pygame.mouse.get_pos()
            
            # CHECK EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit the program
                    print("Closing program, goodbye!")
                    quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                    if menu_buttons[0].under_pointer: # Back button
                        return
                    elif menu_buttons[1].under_pointer: # New savegame button
                        menu_buttons[1].response_function(screen, account_details)
                        loop = False
                        break
                    else: # Check savegame buttons
                        for i, savegame in enumerate(savegame_buttons):
                            if savegame.under_pointer:
                                savegame.response_function(screen) # Open savegame details window
                                
                                # Update time for most recently opened
                                from datetime import datetime
                                now = datetime.now()
                                account_details["savegames"][i]["display_details"]["last_save"] = now.strftime("%d/%m/%Y, %H:%M")
                                loop = False
                                break
            
            # PROCESS
            for button in menu_buttons:
                button.update(mouse_pos)
            for button in savegame_buttons:
                button.update(mouse_pos)
            
            # RENDER
            screen.fill("gray")
            
            # Draw buttons
            for button in menu_buttons:
                screen = button.draw(screen)
            for button in savegame_buttons:
                screen = button.draw(screen)
                
            # Draw text
            screen = draw_text("Savegames", screen, constants.TITLE_FONT, 
                                (constants.DEFAULT_SCREEN_SIZE[0]//2, 70),
                                (0,0,0),
                                "centre", "centre")
            
            pygame.display.flip()

            # Pause for remainder of tick
            time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
