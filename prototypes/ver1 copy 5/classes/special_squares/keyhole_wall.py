
import pygame

class Keyhole:
    def __init__(self, x, y, room_loc, colour):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        self.grid_pos = [x,y]
        self.x_pos = (constants.SQUARE_SIZE[0] * x) + room_loc[0]
        self.y_pos = (constants.SQUARE_SIZE[1] * y) + room_loc[1]
        self.collision_x = self.x_pos
        self.collision_y = self.y_pos
        
        self.width = constants.SQUARE_SIZE[0]
        self.height = constants.SQUARE_SIZE[1]
        
        self.colour = colour
        self.collidable = True
        self.breakable = False
        
        #self.texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/rock.png").convert()
        
        base = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/rock.png").convert()
        temp_surface = pygame.Surface((base.get_width(), base.get_height()), pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(base, (0,0))
        self.texture = temp_surface
        
        temp_surface = pygame.Surface((self.texture.get_width(), self.texture.get_height()), pygame.SRCALPHA)
        temp_surface.blit(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/keyhole_wall.png").convert(), (0,0))
        temp_surface.fill(colour, special_flags=pygame.BLEND_MULT)
        self.texture.blit(temp_surface, (0,0)) 
        
        self.texture = pygame.transform.scale(self.texture, (constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 1.5))
        
        self.draw_loc = [0, -0.5 * constants.SQUARE_SIZE[1]]
        
        
    def save(self):
        return {"id": 12,
                "colour": self.colour}
        
    def get_rendering_row(self):
        return self.y_pos
        
    def draw(self, screen):
        
        temp_surface = pygame.Surface((self.texture.get_width(), self.texture.get_height()), pygame.SRCALPHA)
        temp_surface.blit(self.texture, (0,0))
        
        screen.blit(temp_surface, (self.x_pos + self.draw_loc[0], self.y_pos + self.draw_loc[1]))
        
        return screen