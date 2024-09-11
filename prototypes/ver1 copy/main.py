
def rungame(savegame, config): # Putting within a function so that it will be easier to implement into the main game later
    # Libraries
    import pygame
    import time

    # Local modules
    import classes.menu as menu_classes
    from classes.player import Player

    # Constants
    from classes.global_data import constants_structure
    constants = constants_structure()


    # Used pygame docs: https://www.pygame.org/docs/
    pygame.init()
    screen = pygame.display.set_mode(constants.DEFAULT_SCREEN_SIZE)
    pygame.display.set_caption('Dungeon Game')


    # LOAD LEVEL AND ROOM
    savegameData = savegame
    

    player = Player(constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//2)

    loop = True
    # Main game
    while loop:
        tick_start = time.time()
        
        # FRAME CONSTANTS ONE
        mouse_pos = pygame.mouse.get_pos()
        
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False
            #if event.type == pygame.KEYDOWN:
                
            
        # PROCESS
        player.move(config["key_bindings"], events)
        
        # RENDER
        screen.fill("gray")
        screen = player.draw(screen, config["max_FPS"])
        
        # flip() draws screen to display
        pygame.display.flip()

        # Pause remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))


import json
if __name__ == '__main__':
    with open("projects/prototypes/ver1/data/accounts.json", 'r') as data_file:
        thedata = json.load(data_file)
        savegame = thedata[0]["savegames"][0]
        config = thedata[0]["config"]
        #print(config["key_bindings"])

    rungame(savegame, config)