
def run(screen, key_bindings):
    import pygame
    import time
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    
    
    temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
    temp_surface.fill((100,100,100,100))
    screen.blit(temp_surface, [0,0])
        
        
    loop = True
    while loop:
        tick_start = time.time()
        
        # FRAME CONSTANTS ONE
        mouse_pos = pygame.mouse.get_pos()
        
        
        # CHECK EVENTS
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) == "pause":
                    loop = False
            #if event.type == pygame.KEYDOWN:
                
        
        # RENDER
        
        screen = draw_text("Game Paused", screen, constants.TITLE_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//3], (0,0,0), "centre", "above")
        pause_key = "P" # update to take key from keybindings
        screen = draw_text(f"Press {pause_key} to unpause", screen, constants.NORMAL_FONT, [constants.DEFAULT_SCREEN_SIZE[0]//2, constants.DEFAULT_SCREEN_SIZE[1]//3], (0,0,0), "centre", "below")
        #pygame.draw.rect(temp_surface, (255, 0, 0, 63), (0, 0, 60, 60))
        #screen.fill("gray")
        
        
        # flip() draws screen to display
        pygame.display.flip()

        # Pause remainder of tick
        time.sleep(max(0, (1/constants.MENU_FPS)-(time.time()-tick_start)))
    
    return