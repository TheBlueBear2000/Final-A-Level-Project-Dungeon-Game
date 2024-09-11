def run(screen, account_details):
    print("Logged into account with UUID " + str(account_details["UUID"]) + 
        "\nAccount username is " + account_details["username"])
    
    # Libraries
    import pygame
    import time
    import json

    # Local modules
    import classes.menu as menu_classes
    from functions.loops.savegames import run as savegames
    from functions.loops.options import run as options
    from functions.loops.credits import run as game_credits
    from classes.global_data import constants_structure
    # Constants
    constants = constants_structure()


    # Buttons
    menu_buttons = [
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*3), 
                            size=(600, 100), 
                            text="Savegames", 
                            response_function=savegames,
                        font=constants.TITLE_FONT),
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*4), 
                            size=(600, 100), 
                            text="Options", 
                            response_function=options,
                        font=constants.TITLE_FONT),
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*5), 
                            size=(600, 100), 
                            text="Credits", 
                            response_function=game_credits,
                        font=constants.TITLE_FONT),
        menu_classes.button(location=(10,10), 
                            size=(300, 50), 
                            text="Log Out")
        
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
                        if button == menu_buttons[3]: # Back button
                            return
                        button.response_function(screen, account_details)
                        
                        # reset account details incase of changes
                        with open(constants.FILE_PATH + "data/accounts.json", 'r') as accountsFile:
                            accounts = json.load(accountsFile) 
                            
                        for account in accounts: # find account
                            if account["UUID"] == account_details["UUID"]:
                                account_details = account # save over old account data
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
            
        # Draw text
        content = constants.TITLE_FONT.render("Main Menu", True, (0,0,0))
        screen.blit(content,((constants.DEFAULT_SCREEN_SIZE[0]-content.get_width())//2, int((constants.DEFAULT_SCREEN_SIZE[1]-200)//5*1.5)))
        
        pygame.display.flip()

        # Pause for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
