import copy
import pygame

class Square:
    def __init__(self, square, default, file_path, square_size, location):
        self.data = copy.deepcopy(default)
        for data in square:
            self.data[data] = square[data]
        
        
        from classes.global_data import constants_structure
        constants = constants_structure()
    
        self.collidable = self.data["collidable"]
        
        self.x_pos = location[0]
        self.width = self.data["collision_size"][0] * constants.SQUARE_SIZE[0]
        self.y_pos = location[1]
        self.height = self.data["collision_size"][1] * constants.SQUARE_SIZE[0]
        
        texture_names = self.data["textures"]
        self.textures = [pygame.transform.scale(pygame.image.load(file_path + f"project_lib/assets/squares/{texture_name}.png").convert(), square_size) for texture_name in texture_names]
            

    def draw(self, screen, x_loc, y_loc):
        screen.blit(self.textures[0], (x_loc, y_loc)) # only doing 0 for now, since there are no animations yet
        return screen