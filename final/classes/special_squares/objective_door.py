import pygame
from classes.special_squares.door import Door

class ObjectiveDoor(Door): # Objective Door object extends Door object
    def __init__(self, x, y, hinge_corner, starting_dir, room_location, colour=None, side = None):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Initiate self as Door
        Door.__init__(self, x, y, hinge_corner, starting_dir, room_location, "objective_")
        
        # Set attributes
        self.manual = False
        self.colour = colour
        self.side = side
        self.starting_dir = starting_dir
        
        # Generate textures based on colour
        if colour is not None:
            overlay_textures = {"h": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/squares/objective_door_right_overlay.png").convert(), constants.SQUARE_SIZE),
                                "v": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/squares/objective_door_up_overlay.png").convert(), (constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 2))}
        
            for texture in overlay_textures:
                temp_surface = pygame.Surface((overlay_textures[texture].get_width(), overlay_textures[texture].get_height()), pygame.SRCALPHA)
                temp_surface.blit(overlay_textures[texture], (0,0))
                temp_surface.fill(colour, special_flags=pygame.BLEND_MULT)
                temp_surface_2 = pygame.Surface((self.textures[texture].get_width(), self.textures[texture].get_height()), pygame.SRCALPHA)
                temp_surface_2.blit(self.textures[texture], (0,0))
                temp_surface_2.blit(temp_surface, (0,0))
                self.textures[texture] = temp_surface_2
        
    def save(self):
        # Generate position string
        pos = self.state
        pos += self.corner[0]
        if "left" in self.corner:
            pos += "l"
        else:
            pos += "r"
            
        data = {"id": 9,
                "pos": pos,
                "colour": self.colour}
        return data
