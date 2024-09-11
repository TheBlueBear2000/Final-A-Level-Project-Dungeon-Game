
def rungame(room, config, screen, player, player_loc, level, newlevel, last_room_screenshot): # Putting within a function so that it will be easier to implement into the main game later
    # Libraries
    import pygame
    import time

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
    level_layout = json.load(open(f"projects/prototypes/ver1/data/levels/rooms_{level}/layout.json", 'r'))
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
                doors = json.load(open(f"projects/prototypes/ver1/data/levels/rooms_{level}/{item}.json", 'r'))["doors"]
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
    background.blit(pygame.transform.scale(image, (image.get_width() * 2.5, image.get_height() * 2.5)), (0,0)) #pygame.transform.scale(image, square_size)
    

    # Used pygame docs: https://www.pygame.org/docs/
    


    # LOAD LEVEL AND ROOM
    room = Room(room, level)
    
    #old_player_x_pos = player.x_pos
    #old_player_y_pos = player.y_pos
    #player_coord = [constants.GAME_WINDOW_SIZE[0]//2, constants.GAME_WINDOW_SIZE[1]//2]
    player_coord = [player.x_pos, player.y_pos]
    if player_loc == "right":
        player_coord[0] = room.location[0] + (constants.SQUARE_SIZE[0] * 1.4) - 75
    elif player_loc == "left":
        player_coord[0] = room.location[0] + room.size[0] - (constants.SQUARE_SIZE[0] * 1.4) - 75
    elif player_loc == "bottom":
        player_coord[1] = room.location[1] + (constants.SQUARE_SIZE[1] * 1.4) - 75
    elif player_loc == "top":
        player_coord[1] = room.location[1] + room.size[1] - (constants.SQUARE_SIZE[1] * 1.4) - 75
    #player_coord[0] -= 75
    #player_coord[1] -= 75
    player.teleport(*player_coord)
    
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
    
    player_invisible_start = -60
    
    loop = True
    # Main game
    while loop:
        tick_start = time.time()
        
        from random import randint    
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False, "quit", game_window
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player_invisible_start = frame
            
        # PROCESS
        dead, room.living_items = player.move(config["key_bindings"], 
                    events, 
                    {"layout": room.layout, "location": room.location},
                    room.entities, 
                    room.living_items,
                    room.crates,
                    room.levers,
                    [*room.doors, *room.objective_doors],
                    room,
                    screen)
        if dead:
            room.save()
            player.save(level)
            return True, None, game_window
        
        if player.collision_box["location"][0] <= room.location[0] + (constants.SQUARE_SIZE[0] * 0.6): # If leaving left
            room.save()
            player.save(level)
            return False, "left", game_window
        elif player.collision_box["location"][1] <= room.location[1] + (constants.SQUARE_SIZE[1] * 0.6): # If leaving top
            room.save()
            player.save(level)
            return False, "top", game_window
        elif player.collision_box["location"][0] >= room.location[0] + (len(room.layout[0]) * constants.SQUARE_SIZE[0]) - (constants.SQUARE_SIZE[0] * 0.6): # If leaving right
            room.save()
            player.save(level)
            return False, "right", game_window
        elif player.collision_box["location"][1] >= room.location[1] + (len(room.layout[1]) * constants.SQUARE_SIZE[1]) - (constants.SQUARE_SIZE[1] * 0.6): # If leaving bottom
            room.save()
            player.save(level)
            return False, "bottom", game_window
        
        room.update(player)
        
        for entity in room.entities:
            dead = entity.think(player, room.entities, room.crates, [*room.doors, *room.objective_doors], room, constants) # DEFINE ENTITIES AS ARRAY OF ALL ENTITIES BUT NOT PLAYER
            if dead:
                room.entities.remove(entity)
        
        for item in room.living_items:
            item.move(room.layout, room.location, constants)
            
        for button in room.buttons:
            button.update(player.collision_box, room.crates, room.entities)   
            
        
        if room.ladder is not None:
            if (room.ladder.player_proximity([player.collision_box["location"][i] + 
                                            (player.collision_box["size"][i]//2) for i in range(2)]) 
                <= constants.SQUARE_SIZE[0] // 3):
                print(f"level {level} complete")
                room.save()
                player.save(level)
                return False, "level_complete", game_window
        
        
        # RENDER
        game_window.blit(background, (0,0))
        
        game_window = room.draw(game_window, constants.SQUARE_SIZE, config)
        
        rendering_order = []
        rendering_order = room.get_rendering_list()
        if player_invisible_start + 60 < frame:
            rendering_order.append(player)
        
        rendering_order.sort( key=lambda item : item.get_rendering_row() )
        
        for item in rendering_order:
            game_window = item.draw(game_window)
        
        game_window = room.draw_over(game_window, constants.SQUARE_SIZE)
        
        
        gui_window = player.draw_overlay_data(gui_window, room.location, (len(room.layout[0]) * constants.SQUARE_SIZE[0], len(room.layout[1]) * constants.SQUARE_SIZE[1]))  
        
        #game_window = player.draw(game_window)
        
        gui_window.blit(minimap, ((constants.GUI_WINDOW_SIZE[0] - minimap.get_width())//2, constants.GUI_WINDOW_SIZE[1] * 0.8)) #(room.location[0] + room.size[0] + 100, 450))
        
        if player_invisible_start + 60 < frame:
            game_window = room.draw_icons(game_window, player)
        
        #game_window = player.draw(game_window)
        
        screen.blit(game_window,(0,0))
        
        
        
        
        
        screen.blit(gui_window,(constants.GAME_WINDOW_SIZE[0], 0) if constants.LANDSCAPE else (0, constants.GAME_WINDOW_SIZE[1]))
        frame += 1
        if frame < 25 and newlevel:
            
            temp_surface = pygame.Surface((constants.DEFAULT_SCREEN_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, [50,50,50, 255 - (frame*10)], (0,0, *constants.DEFAULT_SCREEN_SIZE))
            draw_text(f"Level {level}", temp_surface, constants.TITLE_FONT, (constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//2), (255,255,255, 255 - (frame*10)), "centre", "centre")
            screen.blit(temp_surface, (0,0))
            
        
        #thefps = int((1 / processTime)*100)/100
        #draw_text(f"FPS: {thefps}", screen, constants.SMALL_FONT, (10,10), (255,255,255), "left", "below")
        
        # flip() draws screen to display
        pygame.display.flip()

        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
        processTime = time.time()-tick_start


import json
import pygame
if __name__ == '__main__':
    
    account_id = 0
    
    pygame.init()
    screen = pygame.display.set_mode((1000, 720))
    pygame.display.set_caption('Dungeon Game')  
    
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    
    with open(constants.FILE_PATH + "data/accounts.json", 'r') as data_file:
            thedata = json.load(data_file)
            config = thedata[account_id]["config"]
            #print(config["key_bindings"])
    
    level = -1 # 0
    level = 1
    
    
    
    playing = True
    while playing: # in game, between levels
        from classes.player import Player
        player = Player(level, constants.GAME_WINDOW_SIZE[0]//2 - 75, constants.GAME_WINDOW_SIZE[1]//2 - 75)
        
        start_room = 2
        room = json.load(open(constants.FILE_PATH + f"data/levels/rooms_{level}/{start_room}.json", 'r'))
        
        level_layout = json.load(open(constants.FILE_PATH + f"data/levels/rooms_{level}/layout.json", 'r'))
        # find the room coordinates
        for y, row in enumerate(level_layout):
            for x, item in enumerate(row):
                if item == start_room:
                    room_coord = [x, y]
                    break
        
        #player_loc = (constants.DEFAULT_SCREEN_SIZE[0]//2 + 60, constants.DEFAULT_SCREEN_SIZE[1]//2- 120)
        direction = "centre"
        
        dead = False
        newlevel = True
        last_room_screenshot = None
        while not dead: # in level, between rooms
            dead, direction, last_room_screenshot = rungame(room, config, screen, player, direction, level, newlevel, last_room_screenshot)
            newlevel = False
            if dead:
                player.health = player.max_health
                break
            
            if direction == "left":
                room_coord[0] -= 1
            elif direction == "top":
                room_coord[1] -= 1
            elif direction == "right":
                room_coord[0] += 1
            elif direction == "bottom":
                room_coord[1] += 1
            elif direction == "quit":
                playing = False
                break
            else:
                level += 1
                break
            
            room_number = level_layout[room_coord[1]][room_coord[0]]
            #print(room_number)
            #print(direction)
            room = json.load(open(constants.FILE_PATH + f"data/levels/rooms_{level}/{room_number}.json", 'r'))
            
        #player.save(level)