import pygame

class Lever:
    def __init__(self, colour, flicked, location, room_loc):
        from classes.global_data import constants_structure;
        constants = constants_structure()
        
        self.textures = {}
        
        # Generate both textures with colour
        for texture in ["flicked", "unflicked"]:
            base = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/plain_lever_{texture}.png").convert()
            temp_surface = pygame.Surface((base.get_width(), base.get_height()), pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            temp_surface.blit(base, (0,0))
            temp_surface.fill(colour, special_flags=pygame.BLEND_MULT)
            self.textures[texture] = temp_surface
            temp_surface = pygame.Surface((base.get_width(), base.get_height()), pygame.SRCALPHA)
            temp_surface.blit(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/plain_lever_{texture}_rim.png").convert(), (0,0))
            self.textures[texture].blit(temp_surface, (0,0)) 

        
        # Location comes as grid coordinate, so pre-calculate screen coordinates
        self.grid_location = location
        self.x_pos = (location[0] * constants.SQUARE_SIZE[0]) + room_loc[0]
        self.y_pos = (location[1] * constants.SQUARE_SIZE[1]) + room_loc[1]
        self.collision_box = {"size": (constants.SQUARE_SIZE[0] * 0.9, constants.SQUARE_SIZE[1] * 0.9),
                            "location": [self.x_pos + constants.SQUARE_SIZE[0] * 0.05, self.y_pos + constants.SQUARE_SIZE[1] * 0.05]}
        
        # Set other attributes
        self.colour = colour
        self.flicked = flicked
        
    
    def save(self):
        data = {"id": 6,
                "colour": self.colour,
                "flicked": self.flicked}
        return data
    
    def get_rendering_row(self):
        return self.y_pos
    
    def draw(self, screen):
        from classes.global_data import constants_structure;
        constants = constants_structure()
        
        # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface = pygame.Surface(constants.SQUARE_SIZE, pygame.SRCALPHA) 
        
        # Draw depending on state
        if self.flicked:
            temp_surface.blit(pygame.transform.scale(self.textures["flicked"], constants.SQUARE_SIZE),(0,0))
        else:
            temp_surface.blit(pygame.transform.scale(self.textures["unflicked"], constants.SQUARE_SIZE),(0,0))
        
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        return screen
