import pygame
import time

def run(inventory, screen, key_bindings):
    
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    
    # Load textures
    inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory.png").convert(), ((constants.DEFAULT_SCREEN_SIZE[1] * 0.9)//5*3, constants.DEFAULT_SCREEN_SIZE[1] * 0.9))
    square_size = (inv_texture.get_width()//3, inv_texture.get_height()//5)
    inv_location = ((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2, (constants.DEFAULT_SCREEN_SIZE[1] - inv_texture.get_height())//2)
    selected_inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory_highlighted.png").convert(), square_size)
    
    # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
    temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA)
    temp_surface.fill((100,100,100,200))
    screen.blit(temp_surface, [0,0])
    background = screen.copy()
    
    # Loop constants
    selected_item = None
    throw_away_items = []
        
    loop = True
    while loop:
        tick_start = time.time()
        mouse_pos = pygame.mouse.get_pos()
        
        # Calculate what square mouse is on
        selected_square = (((mouse_pos[0] - inv_location[0])//square_size[0]),   (mouse_pos[1] - inv_location[1])//square_size[1]) 
        selected_index = None
        
        # Then calculate what inventory index that square is
        if (selected_square[0] >= 0 and selected_square[0] < 3) and (selected_square[1] >= 0 and selected_square[1] < 4) : # for top 12
            selected_index = selected_square[1] * 3 + selected_square[0] + 2
        elif ((selected_square[0] == 0) or (selected_square[0] == 2)) and (selected_square[1] == 4): # for lower two
            selected_index = selected_square[0]//2
            
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: # Quit program
                print("Closing program, goodbye!")
                quit()
                
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) == "inventory":
                    loop = False # If quit button is pressed
                    
            if event.type == pygame.MOUSEBUTTONUP: # When mouse is released
                if selected_index != None: # If an item is being hovered over
                    if selected_item == None: # If there is no item being held, pick that item up
                        selected_item = inventory[selected_index]
                        inventory[selected_index] = None
                    else: # If there is an item being held, check that the item can be placed in that square
                        temp = None
                        if inventory[selected_index] != None: # Check place is empty
                            temp = inventory[selected_index]
                            
                        do_move = True
                        # Check type fits square
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
                        if do_move: # If all tests pass, place item there
                            inventory[selected_index] = selected_item
                            selected_item = temp
                            
                        
                elif selected_item != None: # If square is not being hovered over, but mouse has an item, then item is being dropped
                    throw_away_items.append(selected_item)
                    selected_item = None
                    
        
        # RENDER
        screen.blit(background, (0,0))
        
        # Draw inventory
        inv_location = ((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width()) //2, (constants.DEFAULT_SCREEN_SIZE[1] - inv_texture.get_height()) //2)
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        temp_surface.blit(inv_texture, inv_location)
        screen.blit(temp_surface, (0,0))
        
        # Draw items
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA)
        # Lower two are handled seperatley 
        if inventory[0] != None:
                temp_surface.blit(pygame.transform.scale(inventory[0].inv_texture, (square_size[0]*0.7, square_size[1]*0.7)), 
                                    (((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2) + square_size[0]*0.15,   (constants.DEFAULT_SCREEN_SIZE[1] + inv_texture.get_height())//2 - square_size[1] + square_size[1]*0.15))
        if inventory[1] != None:
                temp_surface.blit(pygame.transform.scale(inventory[1].inv_texture, (square_size[0]*0.7, square_size[1]*0.7)), 
                                    (((constants.DEFAULT_SCREEN_SIZE[0] - inv_texture.get_width())//2) + (square_size[0] * 2) + square_size[0]*0.15,   (constants.DEFAULT_SCREEN_SIZE[1] + inv_texture.get_height())//2 - square_size[1] + square_size[1]*0.15))
        for i, item in enumerate(inventory[2:]): # Then do all other items
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
        
        # Draw hovered over item indicator
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        if selected_item != None:
            temp_surface.blit(pygame.transform.scale(selected_item.inv_texture, square_size), (mouse_pos[0] - (square_size[0]//2), mouse_pos[1] - (square_size[1]//2)))
        screen.blit(temp_surface, (0,0))
        
        pygame.display.flip()

        # Wait for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
        
    return inventory, throw_away_items
