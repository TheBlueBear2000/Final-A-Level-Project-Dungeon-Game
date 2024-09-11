def run(screen, account_details):
    print("opened options")
    
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    from classes.global_data import constants_structure
    # Constants
    constants = constants_structure()


    # MENU OBJECTS
    menu_buttons = [
        menu_classes.button(location=(10,10), 
                            size=(150, 50), 
                            text="Back",
                            font=constants.NORMAL_FONT)
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
        