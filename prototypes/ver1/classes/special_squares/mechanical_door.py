

import pygame
from classes.special_squares.door import Door

class MechanicalDoor(Door):
    def __init__(self, x, y, hinge_corner, starting_dir, room_location, colour, door_type = "button", objective_side = None, is_open = False):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        Door.__init__(self, x, y, hinge_corner, starting_dir, room_location)
        self.type = door_type
        self.side = objective_side
        self.manual = False
        self.colour = colour
        self.is_open = is_open
        self.starting_dir = starting_dir
        if is_open:
            self.starting_dir = "v"
            if starting_dir == "v":
                self.starting_dir = "h"
            
        
        
        self.textures = {"h": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/squares/mechanical_door_right_base.png").convert(), constants.SQUARE_SIZE),
                        "v": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/squares/mechanical_door_up_base.png").convert(), (constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 2))}
        
        overlay_textures = {"h": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/mechanical_door_right_overlay_{self.type}.png").convert(), constants.SQUARE_SIZE),
                        "v": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/mechanical_door_up_overlay_{self.type}.png").convert(), (constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 2))}
        
        for texture in overlay_textures:
            temp_surface = pygame.Surface((overlay_textures[texture].get_width(), overlay_textures[texture].get_height()), pygame.SRCALPHA)
            temp_surface.blit(overlay_textures[texture], (0,0))
            temp_surface.fill(colour, special_flags=pygame.BLEND_MULT)
            temp_surface_2 = pygame.Surface((self.textures[texture].get_width(), self.textures[texture].get_height()), pygame.SRCALPHA)
            temp_surface_2.blit(self.textures[texture], (0,0))
            temp_surface_2.blit(temp_surface, (0,0))
            self.textures[texture] = temp_surface_2
        
        
            
    def save(self):
        pos = self.state
        pos += self.corner[0]
        if "left" in self.corner:
            pos += "l"
        else:
            pos += "r"
            
        id = 11
        if self.type == "button":
            id = 8
            
        data = {"id": id,
                "pos": pos,
                "open": self.is_open,
                "colour": self.colour}
        return data
        
    