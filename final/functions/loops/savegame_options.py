def open_savegame(account_id, savegame_id, display_data, screen):
    print("editing savegame")
    
    # Libraries
    import pygame
    import time
    from json import load, dump
    
    # Local modules
    import classes.menu as menu_classes
    from classes.global_data import draw_text
    from classes.global_data import constants_structure
    # Constants
    constants = constants_structure()

    # Create background
    over_screen_size = (constants.DEFAULT_SCREEN_SIZE[0]*0.8, constants.DEFAULT_SCREEN_SIZE[1]*0.8)
    over_screen = pygame.Surface(over_screen_size) 
    background_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/buttons/ratio1-2.0.png").convert(), over_screen_size) # Use text input button design
    over_screen.blit(background_texture, (0,0))

    # Buttons
    from game_main import main_game
    from functions.algorithms.delete_savegame import delete_savegame
    menu_buttons = [
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*3), 
                            size=(600, 100), 
                            text="Play", 
                            response_function=main_game,
                            font=constants.TITLE_FONT),
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-300)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*4.5),
                            size=(300,100),
                            text="Delete",
                            response_function=delete_savegame,
                            font=constants.NORMAL_FONT),
        menu_classes.button(location=(constants.DEFAULT_SCREEN_SIZE[0]*0.1 + 10, constants.DEFAULT_SCREEN_SIZE[1]*0.1 + 10), 
                            size=(150, 50), 
                            text="Back")
        
    ]
    
    # shade over menu
    temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
    pygame.draw.rect(temp_surface, (0, 0, 0, 80), (0, 0, *constants.DEFAULT_SCREEN_SIZE))
    screen.blit(temp_surface, (0,0))
    
    loop = True
    tickCount = 0
    while loop:
        tick_start = time.time()
        tickCount += 1
        keysPressed = []
        mouse_pos = pygame.mouse.get_pos()
        
        # CHECK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit progra 
                print("Closing program, goodbye!")
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[2].under_pointer: # Back button
                    return
                
                elif menu_buttons[0].under_pointer:
                    main_game(account_id, savegame_id, screen) # Run game loop
                    return
                
                elif menu_buttons[1].under_pointer:
                    delete_savegame(account_id, savegame_id) # Delete game
                    return
                
            if event.type == pygame.KEYDOWN:
                keysPressed.append(event.unicode) # Track key
        
        # PROCESS
        for button in menu_buttons:
            button.update(mouse_pos, keysPressed)
        
        # RENDER
        # Draw background
        screen.blit(over_screen, (constants.DEFAULT_SCREEN_SIZE[0]*0.1, constants.DEFAULT_SCREEN_SIZE[1]*0.1))
        
        # Draw buttons
        for button in menu_buttons:
            screen = button.draw(screen, tickCount)
        
        # Draw text
        screen = draw_text(display_data["name"], screen, constants.TITLE_FONT, 
                            (constants.DEFAULT_SCREEN_SIZE[0]//2, (constants.DEFAULT_SCREEN_SIZE[1]-over_screen_size[1])//2 + 140),
                            (0,0,0),
                            "centre", "centre")
        
        pygame.display.flip()

        # Wait for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
