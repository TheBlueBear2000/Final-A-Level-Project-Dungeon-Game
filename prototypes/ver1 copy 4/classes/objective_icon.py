
import pygame

class ObjectiveIndicator:
    def __init__(self, side, objective):
        self.side = side
        self.objective = objective
        
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        
        self.texture = temp_surface = pygame.Surface([1,1], pygame.SRCALPHA)
        self.description = []
        if objective["type"] == "kill_count":
            self.texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/icons/skull_and_crossbones.png").convert(), constants.SQUARE_SIZE)
            self.description = [f"Kill a total of {objective['num']}", "enemies to open this door"]
        elif objective["type"] == "keyhole":
            self.texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/icons/key.png").convert(), constants.SQUARE_SIZE)
            self.description = [f"Open this door with a key", "of the matching colour"]
        elif objective["type"] == "powered":
            self.texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/icons/bolt.png").convert(), constants.SQUARE_SIZE)
            self.description = [f"Trigger an input", "of the matching colour"]
        
        if objective["colour"] is not None:
            temp_surface = pygame.Surface((self.texture.get_width(), self.texture.get_height()), pygame.SRCALPHA)
            temp_surface.blit(self.texture, (0,0))
            temp_surface.fill(objective["colour"], special_flags=pygame.BLEND_MULT)
            self.texture = temp_surface
        
        self.centre = [0,0]
        
        if self.side == "left":
            self.centre[0] = constants.SQUARE_SIZE[0] // 2
            self.centre[1] = constants.GAME_WINDOW_SIZE[1] // 2
        elif self.side == "right":
            self.centre[0] = constants.GAME_WINDOW_SIZE[0] - (constants.SQUARE_SIZE[0] // 2)
            self.centre[1] = constants.GAME_WINDOW_SIZE[1] // 2
        elif self.side == "up":
            self.centre[0] = constants.GAME_WINDOW_SIZE[0] // 2
            self.centre[1] = constants.SQUARE_SIZE[1] // 2 + (constants.SQUARE_SIZE[1] // 2)
        elif self.side == "down":
            self.centre[0] = constants.GAME_WINDOW_SIZE[0] // 2
            self.centre[1] = constants.GAME_WINDOW_SIZE[1] - (constants.SQUARE_SIZE[1] // 2)
            
        self.x_pos = self.centre[0] - (self.texture.get_width()//2)
        self.y_pos = self.centre[1] - (self.texture.get_height())
        
    def draw(self, screen, text):
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        temp_surface = pygame.Surface(constants.SQUARE_SIZE, pygame.SRCALPHA)
        temp_surface.blit(self.texture, [0,0])
        screen.blit(temp_surface, [self.x_pos, self.y_pos])
        
        draw_text(text, screen, constants.SMALL_FONT, (self.centre[0], self.centre[1] + (self.texture.get_height()//4)), (255,255,255), "centre", "centre")
        
        from math import sqrt
        mouse_pos = pygame.mouse.get_pos()
        if sqrt(((mouse_pos[0]-self.centre[0])**2) + ((mouse_pos[1]-self.centre[1])**2)) <= constants.SQUARE_SIZE[0] * 1.5:
            temp_surface = pygame.Surface((250, 30 * len(self.description)), pygame.SRCALPHA)
            temp_surface.blit(pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/menu/shadow.png").convert(), (250, 30 * len(self.description))), [0,0])
            
            v_pos = "centre"
            h_pos = "centre"
            if self.side == "left":
                h_pos = "left"
                screen.blit(temp_surface, (mouse_pos[0], mouse_pos[1] - 20))
            elif self.side == "right":
                h_pos = "right"
                screen.blit(temp_surface, (mouse_pos[0] - temp_surface.get_width(), mouse_pos[1] - 20))
            elif self.side == "up":
                v_pos = "below"
                screen.blit(temp_surface, (mouse_pos[0] - (temp_surface.get_width()//2), mouse_pos[1]-5))
            elif self.side == "down":
                v_pos = "above"
                screen.blit(temp_surface, (mouse_pos[0] - (temp_surface.get_width()//2), mouse_pos[1]-20))
            for i, text in enumerate(self.description):
                # draw at fixed pos instead, align accordingly
                draw_text(text, screen, constants.SMALL_FONT, (mouse_pos[0], mouse_pos[1] + (i*20)), (255,255,255), h_pos, v_pos)
        
        return screen