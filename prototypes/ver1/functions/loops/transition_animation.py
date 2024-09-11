
import pygame
import time

def animation(screen, player_loc, game_window, last_room_screenshot, gui_window, background, player):
    from classes.global_data import constants_structure, draw_text
    constants = constants_structure()
    processTime = 1
    
    if player_loc == "top":
        player_loc = "up"
    elif player_loc == "bottom":
        player_loc = "down"
        
    #part_frames = 30
    first_part_frames = 10
    second_part_frames = 20
    
    for frame in range(first_part_frames + second_part_frames): # * 2
        tick_start = time.time()
        screen.blit(background, (0,0))
        if frame <= first_part_frames:
            #player.teleport(player.x_pos - (old_player_x_pos - player_loc[0] // 10),  player.y_pos + (old_player_y_pos - player_loc[1] // 10))
            if player_loc == "up":
                screen.blit(last_room_screenshot, (0, 0 + (frame * (constants.GAME_WINDOW_SIZE[1]//first_part_frames))))
                screen.blit(game_window, (0, 0 - constants.GAME_WINDOW_SIZE[1] + (frame * (constants.GAME_WINDOW_SIZE[1]//first_part_frames))))
            elif player_loc == "down":
                screen.blit(last_room_screenshot, (0, 0 - (frame * (constants.GAME_WINDOW_SIZE[1]//first_part_frames))))
                screen.blit(game_window, (0, constants.GAME_WINDOW_SIZE[1] - (frame * (constants.GAME_WINDOW_SIZE[1]//first_part_frames))))
            elif player_loc == "left":
                screen.blit(last_room_screenshot, (0 + (frame * (constants.GAME_WINDOW_SIZE[0]//first_part_frames)), 0))
                screen.blit(game_window, (0 - constants.GAME_WINDOW_SIZE[0] + (frame * (constants.GAME_WINDOW_SIZE[0]//first_part_frames)), 0))
            elif player_loc == "right":
                screen.blit(last_room_screenshot, (0 - (frame * (constants.GAME_WINDOW_SIZE[0]//first_part_frames)), 0))
                screen.blit(game_window, (constants.GAME_WINDOW_SIZE[0] - (frame * (constants.GAME_WINDOW_SIZE[0]//first_part_frames)), 0))
        else:
            screen.blit(game_window,(0,0))
            # find frame
            anim_frame = (frame-first_part_frames) // 3
            while anim_frame >= len(player.assets[f"run_{player_loc}"]):
                anim_frame -= len(player.assets[f"run_{player_loc}"])
            
            # find position
            pos = [player.x_pos, player.y_pos]
            if player_loc == "up":
                pos[1] = game_window.get_height() - ((frame-first_part_frames) / second_part_frames * (game_window.get_height() - player.y_pos))
            elif player_loc == "down":
                pos[1] =  ((frame-first_part_frames) / second_part_frames * (player.y_pos + player.size[1])) - player.size[1]
            elif player_loc == "left":
                pos[0] = game_window.get_width() - ((frame-first_part_frames) / second_part_frames * (game_window.get_width() - player.x_pos))
            elif player_loc == "right":
                pos[0] = ((frame-first_part_frames) / second_part_frames * (player.x_pos + player.size[0])) - player.size[0]
            screen.blit(player.hand_texture, pos)
            temp_surface = pygame.Surface(player.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            temp_surface.blit(pygame.transform.scale(player.assets[f"run_{player_loc}"][anim_frame], player.size),(0,0))
            screen.blit(temp_surface, pos)



        screen.blit(gui_window,(constants.GAME_WINDOW_SIZE[0], 0) if constants.LANDSCAPE else (0, constants.GAME_WINDOW_SIZE[1]))

        thefps = int((1 / processTime)*100)/100
        draw_text(f"FPS: {thefps}", screen, constants.SMALL_FONT, (10,10), (255,255,255), "left", "below")
        
        # flip() draws screen to display
        pygame.display.flip()
        
        time.sleep(max(0, (1/(constants.MENU_FPS*2))-(time.time()-tick_start)))
        processTime = time.time()-tick_start