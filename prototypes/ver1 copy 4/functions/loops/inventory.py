
import pygame
import time

def run(inventory, screen, key_bindings):
    
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    
    inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory.png").convert(), ((constants.DEFAULT_SCREEN_SIZE[1] * 0.9)//5*3, constants.DEFAULT_SCREEN_SIZE[1] * 0.9))
    square_size = (inv_texture.get_width()//3, inv_texture.get_height()//5)
    inv_location = ((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2, (constants.DEFAULT_SCREEN_SIZE[1] - inv_texture.get_height())//2)
    selected_inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory_highlighted.png").convert(), square_size)
    
    temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
    temp_surface.fill((100,100,100,200))
    screen.blit(temp_surface, [0,0])
    background = screen.copy()
        
    selected_item = None
    
    throw_away_items = []
        
    loop = True
    while loop:
        tick_start = time.time()
        
        # FRAME CONSTANTS ONE
        mouse_pos = pygame.mouse.get_pos()
        
        selected_square = (((mouse_pos[0] - inv_location[0])//square_size[0]),   (mouse_pos[1] - inv_location[1])//square_size[1]) # comes as grid coordinate not screen coordinate
        selected_index = None
        if (selected_square[0] >= 0 and selected_square[0] < 3) and (selected_square[1] >= 0 and selected_square[1] < 4) : # if in main inv, will handle hands later
            selected_index = selected_square[1] * 3 + selected_square[0] + 2
            #print("set selected index to ", selected_index)
        elif ((selected_square[0] == 0) or (selected_square[0] == 2)) and (selected_square[1] == 4): # for lower two
            selected_index = selected_square[0]//2
            #print("set selected index to ", selected_index)
            
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) == "inventory":
                    loop = False
            if event.type == pygame.MOUSEBUTTONUP:
                #print("mouse button up")
                if selected_index != None:
                    #print("index is selected")
                    if selected_item == None:
                        #print("pickup")
                        selected_item = inventory[selected_index]
                        inventory[selected_index] = None
                    else:
                        #print("putdown")
                        temp = None
                        if inventory[selected_index] != None:
                            temp = inventory[selected_index]
                            
                        do_move = True
                        # Not working correctly:
                        #print(selected_item.sort)
                        if selected_index == 8:
                            if selected_item.sort != "ring":
                                do_move = False
                        elif selected_index == 9:
                            if selected_item.sort != "necklace":
                                do_move = False
                        elif selected_index == 10:
                            if selected_item.sort != "bracelet":
                                do_move = False
                        elif selected_index == 11:
                            if selected_item.sort != "helmet":
                                do_move = False
                        elif selected_index == 12:
                            if selected_item.sort != "chestplate":
                                do_move = False
                        elif selected_index == 13:
                            if selected_item.sort != "boots":
                                do_move = False
                        if do_move:
                            inventory[selected_index] = selected_item
                            selected_item = temp
                            
                        
                elif selected_item != None:
                    throw_away_items.append(selected_item)
                    selected_item = None
                    
        
        # RENDER
        screen.blit(background, (0,0))
        
        #screen = draw_text("Inventory", screen, constants.TITLE_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//3], (0,0,0), "centre", "above")
        
        # Inventory
        inv_location = ((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width()) //2, (constants.DEFAULT_SCREEN_SIZE[1] - inv_texture.get_height()) //2)
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        temp_surface.blit(inv_texture, inv_location)
        screen.blit(temp_surface, (0,0))
        
        # Items
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        if inventory[0] != None:
                temp_surface.blit(pygame.transform.scale(inventory[0].inv_texture, (square_size[0]*0.7, square_size[1]*0.7)), 
                                    (((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2) + square_size[0]*0.15,   (constants.DEFAULT_SCREEN_SIZE[1] + inv_texture.get_height())//2 - square_size[1] + square_size[1]*0.15))
        if inventory[1] != None:
                temp_surface.blit(pygame.transform.scale(inventory[1].inv_texture, (square_size[0]*0.7, square_size[1]*0.7)), 
                                    (((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2) + (square_size[0] * 2) + square_size[0]*0.15,   (constants.DEFAULT_SCREEN_SIZE[1] + inv_texture.get_height())//2 - square_size[1] + square_size[1]*0.15))
        for i, item in enumerate(inventory[2:]):
            if item != None:
                temp_surface.blit(pygame.transform.scale(item.inv_texture, (square_size[0]*0.7, square_size[1]*0.7)), 
                                    ((i - (((i)//3)*3)) * square_size[0] + ((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2) + square_size[0]*0.15,   (i)//3 * square_size[1] + ((constants.DEFAULT_SCREEN_SIZE[1] - inv_texture.get_height())//2) + square_size[1]*0.15))
        
        screen.blit(temp_surface, (0,0))
        
        
        # Item hover
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        if (mouse_pos[0] > inv_location[0]  and  mouse_pos[0] < inv_location[0] + (3*square_size[0])  and 
            mouse_pos[1] > inv_location[1]  and  mouse_pos[1] < inv_location[1] + (5*square_size[1])  and  # within boundries
            selected_square != (1, 4)): # dont use empty square
            temp_surface.blit(selected_inv_texture, (selected_square[0] * square_size[0] + inv_location[0], selected_square[1] * square_size[1] + inv_location[1]))
        
        screen.blit(temp_surface, (0,0))
        
        # Held item
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        if selected_item != None:
            temp_surface.blit(pygame.transform.scale(selected_item.inv_texture, square_size), (mouse_pos[0] - (square_size[0]//2), mouse_pos[1] - (square_size[1]//2)))
        screen.blit(temp_surface, (0,0))
        
        
        #pause_key = "P" # update to take key from keybindings
        #screen = draw_text(f"Press {pause_key} to unpause", screen, constants.NORMAL_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//3], (0,0,0), "centre", "below")
        #pygame.draw.rect(temp_surface, (255, 0, 0, 63), (0, 0, 60, 60))
        #screen.fill("gray")
        
        
        # flip() draws screen to display
        pygame.display.flip()

        # Pause remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
    

    return inventory, throw_away_items