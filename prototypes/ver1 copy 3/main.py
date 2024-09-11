
def rungame(room, config): # Putting within a function so that it will be easier to implement into the main game later
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    
    from classes.player import Player
    from classes.entities.enemy import Enemy
    from classes.entities.enemies.goblin import Goblin
    from classes.items.living_item import LivingItem
    
    from classes.items.stick import StickSword
    
    from classes.room import Room

    # Constants
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()


    # Used pygame docs: https://www.pygame.org/docs/
    pygame.init()
    screen = pygame.display.set_mode(constants.DEFAULT_SCREEN_SIZE)
    pygame.display.set_caption('Dungeon Game')  


    # LOAD LEVEL AND ROOM
    room = Room(room)
        

    player = Player(constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//2)
    
    entities = [Goblin(constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//2 - 120),
                Goblin(constants.DEFAULT_SCREEN_SIZE[0]//2 + 60, constants.DEFAULT_SCREEN_SIZE[1]//2 - 150)]
    
    living_items = [LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 180, constants.DEFAULT_SCREEN_SIZE[1]//2, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 170, constants.DEFAULT_SCREEN_SIZE[1]//2+50, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 200, constants.DEFAULT_SCREEN_SIZE[1]//2+30, StickSword()),
                    LivingItem(constants.DEFAULT_SCREEN_SIZE[0]//2 - 1500, constants.DEFAULT_SCREEN_SIZE[1]//2-20, StickSword())]

    loop = True
    # Main game
    while loop:
        tick_start = time.time()
        
        from random import randint
        if randint(0, 50) == 0:
            entities.append(Goblin(constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//2 - 120))
        
        #print()
        #print()
        
        # FRAME CONSTANTS ONE
        mouse_pos = pygame.mouse.get_pos()
        
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False
            #if event.type == pygame.KEYDOWN:
                
            
        # PROCESS
        dead, living_items = player.move(config["key_bindings"], 
                    events, 
                    {"layout": room.layout, "location": room.location},
                    entities, 
                    living_items,
                    room,
                    screen)
        if dead:
            break
        for entity in entities:
            dead = entity.think(player, entities, room, constants) # DEFINE ENTITIES AS ARRAY OF ALL ENTITIES BUT NOT PLAYER
            if dead:
                entities.remove(entity)
        
        for item in living_items:
            item.move(room.layout, room.location, constants)
        
        
        #from functions.algorithms.a_star_pathfind import a_star
        
        #path = a_star([2,6], [player.collision_box["location"][0] + (player.collision_box["size"][0]//2), player.collision_box["location"][1] + (player.collision_box["size"][1]//2)], room)
        # path = a_star([2,6], player.collision_box["location"], room)
        
        # RENDER
        screen.fill("gray")
        screen = room.draw(screen, constants.SQUARE_SIZE)
        
        for entity in entities:
            screen = entity.draw(screen, config["max_FPS"])
        
        for item in living_items:
            screen = item.draw(screen)
        
        screen = player.draw_overlay_data(screen, room.location, (len(room.layout[0]) * constants.SQUARE_SIZE[0], len(room.layout[1]) * constants.SQUARE_SIZE[1]))  
        
        screen = player.draw(screen, config["max_FPS"])
        
        #print(entities[0].state)
        
        #temp_surface = pygame.Surface([60,60], pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        #pygame.draw.rect(temp_surface, (255, 0, 0, 63), (0, 0, 60, 60))
        #for i, square in enumerate(path):
        #    screen = draw_text(str(i), screen, constants.SMALL_FONT, square, (0,0,0), "left", "below")
        #    screen.blit(temp_surface, square)
            
        
        
        # flip() draws screen to display
        pygame.display.flip()

        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))


import json
if __name__ == '__main__':
    with open("projects/prototypes/ver1/data/accounts.json", 'r') as data_file:
        thedata = json.load(data_file)
        config = thedata[0]["config"]
        #print(config["key_bindings"])
        
    room = json.load(open("projects/prototypes/ver1/data/levels/rooms_0/0.json", 'r'))

    rungame(room, config)