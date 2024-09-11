def save_buttons_to_options(menu_buttons, account_details):
    
    keybindings = {}
    for button in menu_buttons[1:]: # buttons not including back button
        keybindings[ord(button.key)] = button.name
        
    # Re-include other keys that do not have buttons
    keybindings["1073742049"] = "sprint"
    keybindings["L_CLICK"] = "attack"
    
    # Update account details
    account_details["config"]["key_bindings"] = keybindings
    
    # Save over account with new details
    import json
    from classes.global_data import constants_structure
    constants = constants_structure()
    
    # get accounts
    with open(constants.FILE_PATH + "data/accounts.json", 'r') as accountsFile:
        accounts = json.load(accountsFile)
        
    for i, account in enumerate(accounts): # find account
        if account["UUID"] == account_details["UUID"]:
            accounts[i] = account_details # save over old account
            
    # save file
    with open(constants.FILE_PATH + "data/accounts.json", 'w') as accountsFile:
        json.dump(accounts, accountsFile, indent=4)
        accountsFile.close()
    
    return account_details


def run(screen, account_details):
    print("opened options")
    
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    from classes.global_data import constants_structure, draw_text
    # Constants
    constants = constants_structure()
    
    # Buttons
    menu_buttons = [
        menu_classes.button(location=(10,10), 
                            size=(150, 50), 
                            text="Back",
                            font=constants.NORMAL_FONT)
    ]       
    
    # Generate buttons based off of keys
    listed_bindings = {}
    for key in account_details["config"]["key_bindings"]:
        if key.isnumeric() and int(key) < 110000: # not including attack key or sprint key
            listed_bindings[key] = account_details["config"]["key_bindings"][key]
            
    for i, key in enumerate(listed_bindings):
        menu_buttons.append(menu_classes.KeyBindingInput(location=(constants.DEFAULT_SCREEN_SIZE[0]//2 - 100  if i < len(listed_bindings)//2 else constants.DEFAULT_SCREEN_SIZE[0] - 100, ((constants.DEFAULT_SCREEN_SIZE[1]+ 30)//(len(listed_bindings)//2+4)*((i if i < len(listed_bindings)//2 else i - (len(listed_bindings)//2))+2))+ 50), 
                                                        size=(75,75),
                                                        name=listed_bindings[key],
                                                        key=chr(int(key))))

    # SPACE TO ADD MORE OPTIONS BUTTONS
        
    displayedError = None
    current_button = None
    tickCount = 0
    
    loop = True
    while loop:
        tick_start = time.time()
        tickCount += 1
        mouse_pos = pygame.mouse.get_pos()
        
        # CHECK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit program
                save_buttons_to_options(menu_buttons, account_details)
                print("Closing program, goodbye!")
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN: # Check buttons being pressed
                if menu_buttons[0].under_pointer: # Back button
                    save_buttons_to_options(menu_buttons, account_details) # Save before menu is quit
                    return 
                
                a_button_pressed = False
                for i, button in enumerate(menu_buttons):
                    if button.under_pointer:
                        if button.response_function(): # Will return true if the button is being selected (false if being unselected)
                            current_button = i
                            a_button_pressed = True
                        else:
                            current_button = None # If button is deselected, there is no button
                    else:
                        button.selected = False
                        
                if not a_button_pressed:
                    current_button = None
                            
            if event.type == pygame.KEYDOWN:
                if current_button is not None:
                    if event.key < 110000:
                        key = chr(event.key)
                        # Check that key is not in use
                        possible = True
                        for button in menu_buttons[1:]:
                            if button.key == key and button != menu_buttons[current_button]:
                                possible = False
                                break
                        if possible: # Key is usable so change button data
                            menu_buttons[current_button].key = key
                            menu_buttons[current_button].selected = False
                            current_button = None
                        else: # Create error if key cannot be changed
                            displayedError = menu_classes.displayedError("This key is already in use", tickCount)
                        
        # PROCESS
        for button in menu_buttons:
            button.update(mouse_pos)
        
        # RENDER
        screen.fill("gray")
        
        # Draw error
        if displayedError != None:
            screen = displayedError.draw(screen)
        
        # Draw buttons
        for button in menu_buttons:
            screen = button.draw(screen)
            
        # Draw text
        screen = draw_text("Options", screen, constants.TITLE_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//5], (0,0,0), "centre", "above")
        screen = draw_text("Keybindings", screen, constants.NORMAL_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//5], (0,0,0), "centre", "below")
        
        pygame.display.flip()

        # Pause for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
