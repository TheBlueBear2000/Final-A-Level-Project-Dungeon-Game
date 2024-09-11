def load_new_savegame(constants, game_id, name="Untitled Savegame"):
    from json import load
    from datetime import datetime
    now = datetime.now()
    
    # Get default savegame data
    with open(constants.FILE_PATH + "data/default_savegame.json", "r") as default_file:
        default_json = load(default_file)
    
    # Set display data and ID
    default_json["display_details"]["name"] = name
    default_json["display_details"]["id"] = game_id
    default_json["display_details"]["last_save"] = "Not saved"
    default_json["display_details"]["created"] = now.strftime("%d/%m/%Y") # Get current time
    
    print("created new savegame called \"" + name + "\"")
    return default_json

def create_new_game_files(account_id, destination_level_id):
    import shutil
    from classes.global_data import constants_structure
    constants = constants_structure()

    # Create files
    shutil.copytree(constants.FILE_PATH + f"data/account_games/default_games/default_levels",  # source
                    constants.FILE_PATH + f"data/account_games/{account_id}_games/{destination_level_id}_levels")  # destination

def entry_loop(screen, account_details):
    print("creating new savegame")
    
    import pygame
    import time
    from json import dump, load
    
    import classes.menu as menu_classes
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()

    # Define sub-window
    over_screen_size = (constants.DEFAULT_SCREEN_SIZE[0]*0.8, constants.DEFAULT_SCREEN_SIZE[1]*0.8)
    over_screen = pygame.Surface(over_screen_size) 
    background_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/buttons/ratio1-2.0.png").convert(), over_screen_size) # Use text input button design
    over_screen.blit(background_texture, (0,0))

    # Buttons
    menu_buttons = [
        menu_classes.button(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*5), 
                            size=(600, 100), 
                            text="Create Savegame", 
                            response_function=load_new_savegame,
                            font=constants.TITLE_FONT),
        menu_classes.textInputBox(location=((constants.DEFAULT_SCREEN_SIZE[0]-600)//2, (constants.DEFAULT_SCREEN_SIZE[1]-200)//5*3),
                            size=(600,100),
                            button_name="Name"),
        menu_classes.button(location=(constants.DEFAULT_SCREEN_SIZE[0]*0.1 + 10, constants.DEFAULT_SCREEN_SIZE[1]*0.1 + 10), 
                            size=(150, 50), 
                            text="Back")
        
    ]
    
    # Shade over previous window
    temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
    pygame.draw.rect(temp_surface, (0, 0, 0, 80), (0, 0, *constants.DEFAULT_SCREEN_SIZE))
    screen.blit(temp_surface, (0,0))
    
    
    
    loop = True
    tickCount = 0
    while loop: # Window loop
        tick_start = time.time()
        tickCount += 1
        keysPressed = []
        mouse_pos = pygame.mouse.get_pos()
        
        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit program if window closed
                print("Closing program, goodbye!")
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[2].under_pointer: # Back button
                    return
                
                elif menu_buttons[0].under_pointer: # Create game button
                    game_id = account_details["savegames"][len(account_details["savegames"])-1]["display_details"]["id"] + 1 # automatically makes the ID 1 larger than the largest ID saved (which will always be the last one)
                    account_details["savegames"].append(load_new_savegame(constants, game_id, menu_buttons[1].content))
                    # resave account - TURN THIS INTO SAVE FUNCTION WHEN ACCOUNT OBJECT IS CREATED
                    with open(constants.FILE_PATH + "data/accounts.json", 'r+') as accountsDB:
                        accountsDBJson = load(accountsDB)
                        for i, account in enumerate(accountsDBJson):
                            if account["UUID"] == account_details["UUID"]:
                                accountsDBJson[i] = account_details
                        accountsDB.seek(0)
                        dump(accountsDBJson, accountsDB, indent=4)
                        accountsDB.close()
                        
                    create_new_game_files(account_details["UUID"], game_id)
                    
                    return
                
                elif menu_buttons[1].under_pointer: # Name input box
                    menu_buttons[1].response_function()
                else:
                    menu_buttons[1].selected = False
                
            if event.type == pygame.KEYDOWN:
                keysPressed.append(event.unicode) # Track keys pressed for text input
        
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
        screen = draw_text("New Savegame", screen, constants.TITLE_FONT, 
                            (constants.DEFAULT_SCREEN_SIZE[0]//2, (constants.DEFAULT_SCREEN_SIZE[1]-over_screen_size[1])//2 + 70),
                            (0,0,0),
                            "centre", "centre")
        
        pygame.display.flip()

        # Wait for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
