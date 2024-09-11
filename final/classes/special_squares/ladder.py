import pygame

class Ladder:
    def __init__(self, x, y, room_loc):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        self.texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/ladder.png").convert(), constants.SQUARE_SIZE)
        
        # Pre-calculate screen coordinates from grid coordinates
        self.grid_coords = (x, y)
        self.x_pos = (x * constants.SQUARE_SIZE[0]) + room_loc[0]
        self.y_pos = (y * constants.SQUARE_SIZE[1]) + room_loc[1]
    
    def player_proximity(self, player_loc):
        from math import sqrt
        
        # Use Pythagoras's theorem to calculate direct distance from the player
        return sqrt(((player_loc[0] - self.x_pos - (self.texture.get_width()//2))**2) + ((player_loc[1] - self.y_pos - (self.texture.get_height()//2))**2))
        
    def get_rendering_row(self):
        return self.y_pos
        
    def draw(self, screen):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        temp_surface = pygame.Surface((constants.SQUARE_SIZE), pygame.SRCALPHA)
        temp_surface.blit(self.texture, [0,0])
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        return screen
