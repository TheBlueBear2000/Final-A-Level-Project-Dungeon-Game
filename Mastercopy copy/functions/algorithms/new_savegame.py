
def load_new_savegame(constants, name="Untitled Savegame"):
    from json import load
    from datetime import datetime
    now = datetime.now()
    
    with open(constants.FILE_PATH + "data/default_savegame.json", "r") as default_file:
        default_json = load(default_file)
        
    default_json["display_details"]["name"] = name
    default_json["display_details"]["last_save"] = now.strftime("%d/%m/%Y, %H:%M")
    default_json["display_details"]["created"] = now.strftime("%d/%m/%Y")
    
    print("created new savegame called \"" + name + "\"")
    return default_json





def entry_loop(screen, account_details):
    print("creating new savegame")
    
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

    over_screen_size = (constants.DEFAULT_SCREEN_SIZE[0]*0.8, constants.DEFAULT_SCREEN_SIZE[1]*0.8)
    over_screen = pygame.Surface(over_screen_size) 

    # MENU OBJECTS
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
        
        # FRAME CONSTANTS ONE
        mouse_pos = pygame.mouse.get_pos()
        
        # CHECK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[2].under_pointer:
                    return
                
                elif menu_buttons[0].under_pointer:
                    account_details["savegames"].append(menu_buttons[0].response_function(constants, menu_buttons[1].content))
                    # resave account - TURN THIS INTO SAVE FUNCTION WHEN ACCOUNT OBJECT IS CREATED
                    with open(constants.FILE_PATH + "data/accounts.json", 'r+') as accountsDB:
                        accountsDBJson = load(accountsDB)
                        for i, account in enumerate(accountsDBJson):
                            if account["UUID"] == account_details["UUID"]:
                                accountsDBJson[i] = account_details
                        accountsDB.seek(0)
                        dump(accountsDBJson, accountsDB, indent=4)
                        accountsDB.close()
                    return
                
                elif menu_buttons[1].under_pointer:
                    menu_buttons[1].response_function()
                else:
                    menu_buttons[1].selected = False
                
            if event.type == pygame.KEYDOWN:
                keysPressed.append(event.unicode)
        
        # PROCESS
        for button in menu_buttons:
            button.update(mouse_pos, keysPressed)
        
        # RENDER
        screen.blit(over_screen, (constants.DEFAULT_SCREEN_SIZE[0]*0.1, constants.DEFAULT_SCREEN_SIZE[1]*0.1))
        
        over_screen.fill("gray")
        for button in menu_buttons:
            screen = button.draw(screen, tickCount)
        
        screen = draw_text("New Savegame", screen, constants.TITLE_FONT, 
                            (constants.DEFAULT_SCREEN_SIZE[0]//2, (constants.DEFAULT_SCREEN_SIZE[1]-over_screen_size[1])//2 + 70),
                            (0,0,0),
                            "centre", "centre")
        
        # flip() draws screen to display
        pygame.display.flip()

        # Pause remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
        