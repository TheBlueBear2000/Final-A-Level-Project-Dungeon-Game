def rungame(account_id, savegame_id, room, config, screen, player, player_loc, level, newlevel, last_room_screenshot):
    # Libraries
    import pygame
    import time
    from random import randint

    # Local modules
    import classes.menu as menu_classes
    
    from classes.player import Player
    from classes.room import Room

    # Constants
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    
    # define game and GUI subwindows
    game_window = pygame.Surface((constants.GAME_WINDOW_SIZE), pygame.SRCALPHA)
    gui_window = pygame.Surface((constants.GUI_WINDOW_SIZE), pygame.SRCALPHA)
    
    # draw minimap image
    map_room_size = [20,20]
    map_joint_length = 10
    map_joint_width = 7
    level_layout = json.load(open(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels/rooms_{level}/layout.json", 'r'))
    minimap = pygame.Surface(((len(level_layout[0]) * (map_room_size[0] + map_joint_length)) - map_joint_length,   (len(level_layout) * (map_room_size[1] + map_joint_length)) - map_joint_length), pygame.SRCALPHA)
    # draw squares
    for y, row in enumerate(level_layout):
        for x, item in enumerate(row):
            if item != 0:
                # squares
                pygame.draw.rect(minimap, (0,0,0), (x * (map_room_size[0] + map_joint_length), y * (map_room_size[1] + map_joint_length), *map_room_size))
                if room["id"] == item:
                    pygame.draw.circle(minimap, (255,255,255), ((x * (map_room_size[0] + map_joint_length)) + (map_room_size[0]//2), (y * (map_room_size[1] + map_joint_length))+ (map_room_size[1]//2)), map_room_size[0]//3)
                
                # lines
                doors = json.load(open(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels/rooms_{level}/{item}.json", 'r'))["doors"]
                if doors["right"] is not None:
                    colour = (100,100,100)
                    if doors["right"]["complete"]:
                        colour = (0,0,0)
                    pygame.draw.rect(minimap, colour, ((x * (map_room_size[0] + map_joint_length)) + map_room_size[0], (y * (map_room_size[1] + map_joint_length)) + ((map_room_size[1]-map_joint_width)//2), map_joint_length, map_joint_width))
                if doors["down"] is not None:
                    colour = (100,100,100)
                    if doors["down"]["complete"]:
                        colour = (0,0,0)
                    pygame.draw.rect(minimap, colour, ((x * (map_room_size[0] + map_joint_length)) + ((map_room_size[0]-map_joint_width)//2), (y * (map_room_size[1] + map_joint_length)) + map_room_size[0], map_joint_width, map_joint_length))
    
    # get background
    background = pygame.Surface(constants.GAME_WINDOW_SIZE)
    image = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/underground_background.png").convert()
    background.blit(pygame.transform.scale(image, (image.get_width() * 2.5, image.get_height() * 2.5)), (0,0))
    

    # Load room
    room = Room(room, level, {"account_id": account_id, "savegame_id": savegame_id})
    
    # Load player starting position
    player_coord = [player.x_pos, player.y_pos]
    if player_loc == "right":
        player_coord[0] = room.location[0] + (constants.SQUARE_SIZE[0] * 1.4) - 75
    elif player_loc == "left":
        player_coord[0] = room.location[0] + room.size[0] - (constants.SQUARE_SIZE[0] * 1.4) - 75
    elif player_loc == "bottom":
        player_coord[1] = room.location[1] + (constants.SQUARE_SIZE[1] * 1.4) - 75
    elif player_loc == "top":
        player_coord[1] = room.location[1] + room.size[1] - (constants.SQUARE_SIZE[1] * 1.4) - 75
    player.teleport(*player_coord)
    
    # Run transition animation to new room
    if not newlevel:
        game_window = room.draw(game_window, constants.SQUARE_SIZE, config)
        rendering_order = sorted(room.get_rendering_list(), key=lambda item : item.get_rendering_row() )
        for item in rendering_order:
            game_window = item.draw(game_window)
            
        gui_window = player.draw_overlay_data(gui_window, room.location, (len(room.layout[0]) * constants.SQUARE_SIZE[0], len(room.layout[1]) * constants.SQUARE_SIZE[1]))  
        gui_window.blit(minimap, ((constants.GUI_WINDOW_SIZE[0] - minimap.get_width())//2, constants.GUI_WINDOW_SIZE[1] * 0.8))
        game_window = room.draw_over(game_window, constants.SQUARE_SIZE)
        from functions.loops.transition_animation import animation
        animation(screen, player_loc, game_window, last_room_screenshot, gui_window, background, player)
    
    player.reassess_keys(config["key_bindings"])
    

    processTime = 1
    
    frame = 0
    
    loop = True
    # Main game
    while loop:
        tick_start = time.time()

        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # Always save before program quits
                player.save(level, room.id)
                room.save()
                print("Closing program, goodbye!")
                quit()
            
        # PROCESS
        # Move player
        dead, room.living_items, continue_game = player.move(config["key_bindings"], 
                    events, 
                    {"layout": room.layout, "location": room.location},
                    room.entities, 
                    room.living_items,
                    room.crates,
                    room.levers,
                    [*room.doors, *room.objective_doors],
                    room,
                    screen)
        
        if not continue_game: # If the game needs to be quit, save progress and exit
            player.save(level, room.id)
            room.save()
            return False, "quit", game_window
            
        if dead: # If the player has died, handle as such
            player.lives -= 1
            if player.lives < 0:
                return True, "final_death", game_window # Restart whole level on final death
            
            # If theres still lives left, respawn at start
            player.health = player.max_health
            player.x_pos = constants.GAME_WINDOW_SIZE[0]//2 - 75
            player.y_pos = constants.GAME_WINDOW_SIZE[1]//2 - 75
            room.save()
            player.save(level, 1)
            return True, None, game_window
        
        # Check if player is at gateway to neighboring room
        if player.collision_box["location"][0] <= room.location[0] + (constants.SQUARE_SIZE[0] * 0.6): # If leaving left
            room.save()
            player.save(level, room.id)
            return False, "left", game_window
        elif player.collision_box["location"][1] <= room.location[1] + (constants.SQUARE_SIZE[1] * 0.6): # If leaving top
            room.save()
            player.save(level, room.id)
            return False, "top", game_window
        elif player.collision_box["location"][0] >= room.location[0] + (len(room.layout[0]) * constants.SQUARE_SIZE[0]) - (constants.SQUARE_SIZE[0] * 0.6): # If leaving right
            room.save()
            player.save(level, room.id)
            return False, "right", game_window
        elif player.collision_box["location"][1] >= room.location[1] + (len(room.layout[1]) * constants.SQUARE_SIZE[1]) - (constants.SQUARE_SIZE[1] * 0.6): # If leaving bottom
            room.save()
            player.save(level, room.id)
            return False, "bottom", game_window
        
        # Update room
        room.update(player)
        
        # Update entities
        for entity in room.entities:
            dead = entity.think(player, room.entities, room.crates, [*room.doors, *room.objective_doors], room, constants) # DEFINE ENTITIES AS ARRAY OF ALL ENTITIES BUT NOT PLAYER
            if dead:
                room.entities.remove(entity)
        
        for item in room.living_items:
            item.move(room.layout, room.location, constants)
            
        # Update squares
        for button in room.buttons:
            button.update(player.collision_box, room.crates, room.entities)   
            
        if room.ladder is not None:
            if (room.ladder.player_proximity([player.collision_box["location"][i] + 
                                            (player.collision_box["size"][i]//2) for i in range(2)]) 
                <= constants.SQUARE_SIZE[0] // 3):
                print(f"level {level} complete")
                room.save()
                player.save(level, room.id)
                return False, "level_complete", game_window # Move to next level if player has completed it
        
        # RENDER
        game_window.blit(background, (0,0))
        
        # Draw room
        game_window = room.draw(game_window, constants.SQUARE_SIZE, config)
        
        # Calculate rendering order
        rendering_order = []
        rendering_order = room.get_rendering_list()
        rendering_order.append(player)
        rendering_order.sort( key=lambda item : item.get_rendering_row() )
        
        # Draw rendering order
        for item in rendering_order:
            game_window = item.draw(game_window)
        
        # Draw room overlays
        game_window = room.draw_over(game_window, constants.SQUARE_SIZE)
        game_window = room.draw_icons(game_window, player)
        
        # Draw GUI window
        gui_window = player.draw_overlay_data(gui_window, room.location, (len(room.layout[0]) * constants.SQUARE_SIZE[0], len(room.layout[1]) * constants.SQUARE_SIZE[1]))  
        gui_window.blit(minimap, ((constants.GUI_WINDOW_SIZE[0] - minimap.get_width())//2, constants.GUI_WINDOW_SIZE[1] * 0.8)) #(room.location[0] + room.size[0] + 100, 450))
        
        
        # Draw seperate subwindows to main display
        screen.blit(game_window,(0,0))
        screen.blit(gui_window,(constants.GAME_WINDOW_SIZE[0], 0) if constants.LANDSCAPE else (0, constants.GAME_WINDOW_SIZE[1]))
        
        # Draw new level overlay for new levels
        if frame < 25 and newlevel:
            frame += 1
            temp_surface = pygame.Surface((constants.DEFAULT_SCREEN_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, [50,50,50, 255 - (frame*10)], (0,0, *constants.DEFAULT_SCREEN_SIZE))
            draw_text(f"Level {level}", temp_surface, constants.TITLE_FONT, (constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//2), (255,255,255, 255 - (frame*10)), "centre", "centre")
            screen.blit(temp_surface, (0,0))
            
        # Draw FPS
        thefps = int((1 / processTime)*100)/100
        draw_text(f"FPS: {thefps}", screen, constants.SMALL_FONT, (10,10), (255,255,255), "left", "below")
        
        pygame.display.flip()
        
        # Wait for remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
        processTime = time.time()-tick_start


import json
import pygame
def main_game(account_id, savegame_id, screen): # Runs level system and room system
    print(f"running account {account_id} game {savegame_id}")
    
    from classes.global_data import constants_structure
    constants = constants_structure()
    
    # Extract account data
    with open(constants.FILE_PATH + "data/accounts.json", 'r') as data_file:
            thedata = json.load(data_file)
            config = thedata[account_id - 1]["config"]
    
    level = 1 # Start game at level 1
    
    
    playing = True
    while playing: # In game loop, switches between levels
        from classes.player import Player
        player = Player(level, account_id, savegame_id)
        
        # Load room
        room = json.load(open(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels/rooms_{level}/{player.current_room}.json", 'r'))
        
        # Find the current room coordinates
        level_layout = json.load(open(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels/rooms_{level}/layout.json", 'r'))
        for y, row in enumerate(level_layout):
            for x, item in enumerate(row):
                if item == player.current_room:
                    room_coord = [x, y]
                    break
        
        direction = "centre"
        
        dead = False
        newlevel = True
        last_room_screenshot = None
        while not dead: # In level loop, switches between rooms
            # Run actual game
            dead, direction, last_room_screenshot = rungame(account_id, savegame_id, room, config, screen, player, direction, level, newlevel, last_room_screenshot)
            newlevel = False
            if dead: 
                if direction == "final_death": # On final death, reset level data and then continue to restart level, since data is new
                    # Remove old files
                    from shutil import rmtree
                    rmtree(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels")
                    
                    # Create new files from template
                    from functions.algorithms.new_savegame import create_new_game_files
                    create_new_game_files(account_id, savegame_id)
                    
                break # Restart level if dead
            
            # Switch rooms
            if direction == "left":
                room_coord[0] -= 1
            elif direction == "top":
                room_coord[1] -= 1
            elif direction == "right":
                room_coord[0] += 1
            elif direction == "bottom":
                room_coord[1] += 1
                
            # Quit game
            elif direction == "quit": 
                playing = False
                break
            
            # Next level
            else:
                level += 1
                break
            
            # Get data for next room
            room_number = level_layout[room_coord[1]][room_coord[0]]
            room = json.load(open(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels/rooms_{level}/{room_number}.json", 'r'))
