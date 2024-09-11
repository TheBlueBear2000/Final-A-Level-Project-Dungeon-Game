def run(screen, account_details):
    print("opened savegames")
    
    
    # COULD ADD:
    # - scroller bar for savegames
    # - delete savegame button, with confirmation screen
    # - rename savegame button
    
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
        # MENU OBJECTS
        index = -1
        savegame_buttons = []
        savegame_button_size = (400, 200)
        for i, savegame in enumerate(account_details["savegames"]):
            if i%2 == 0:
                x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) - savegame_button_size[0] - 5
            else:
                x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) + 5
            savegame_buttons.append(menu_classes.savegameButton(( x_loc, 150 + ((len(savegame_buttons)//2) * (savegame_button_size[1] + 15)) ), 
                                                                savegame_button_size, 
                                                                savegame["display_details"]))
            index = i
        
        index += 1
        if index%2 == 0:
            x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) - savegame_button_size[0] - 5
        else:
            x_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2) + 5
        new_savegame_location = ( x_loc, 
                                150 + ((len(savegame_buttons)//2) * (savegame_button_size[1] + 15)) )
        
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
            
            # FRAME CONSTANTS ONE
            mouse_pos = pygame.mouse.get_pos()
            
            # CHECK EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                    if menu_buttons[0].under_pointer:
                        return
                    elif menu_buttons[1].under_pointer:
                        menu_buttons[1].response_function(screen, account_details)
                        loop = False
                        break
            
            # PROCESS
            for button in menu_buttons:
                button.update(mouse_pos)
                
            for button in savegame_buttons:
                button.update(mouse_pos)
            
            # RENDER
            screen.fill("gray")
            for button in menu_buttons:
                screen = button.draw(screen)
            
            for button in savegame_buttons:
                screen = button.draw(screen)
                
            screen = draw_text("Savegames", screen, constants.TITLE_FONT, 
                                (constants.DEFAULT_SCREEN_SIZE[0]//2, 70),
                                (0,0,0),
                                "centre", "centre")
            
            
            # flip() draws screen to display
            pygame.display.flip()

            # Pause remainder of tick
            time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
    