import pygame

class Button:
    def __init__(self, colour, location, room_loc):
        from classes.global_data import constants_structure;
        constants = constants_structure()
        
        self.textures = {}
        
        # Add pressed and unpressed textures
        for texture in ["up", "down"]:
            base = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/plain_button_{texture}.png").convert()
            temp_surface = pygame.Surface((base.get_width(), base.get_height()), pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
            temp_surface.blit(base, (0,0))
            temp_surface.fill(colour, special_flags=pygame.BLEND_MULT)
            self.textures[texture] = temp_surface
            temp_surface = pygame.Surface((base.get_width(), base.get_height()), pygame.SRCALPHA)
            temp_surface.blit(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/plain_button_{texture}_rim.png").convert(), (0,0))
            self.textures[texture].blit(temp_surface, (0,0)) 
        
        # Location comes as grid coordinate, so translate it to screen coordinate
        self.grid_location = location
        self.x_pos = (location[0] * constants.SQUARE_SIZE[0]) + room_loc[0]
        self.y_pos = (location[1] * constants.SQUARE_SIZE[1]) + room_loc[1]
        self.collision_box = {"size": (constants.SQUARE_SIZE[0] * 0.9, constants.SQUARE_SIZE[1] * 0.9),
                            "location": [self.x_pos + constants.SQUARE_SIZE[0] * 0.05, self.y_pos + constants.SQUARE_SIZE[1] * 0.05]}
        
        # Set attributes
        self.colour = colour
        self.state_up = True
        
        
    def update(self, player_collision_box, crates, enemies): # Runs every tick
        from functions.algorithms.collision_detection import collision
        self.state_up = True
        
        # Check if player is pressing it
        if collision([*player_collision_box["location"], *player_collision_box["size"]], [*self.collision_box["location"], *self.collision_box["size"]]):
            self.state_up = False
        else:
            for crate in crates: # Check if crate is pressing it
                if collision([*crate.collision_box["location"], *crate.collision_box["size"]], [*self.collision_box["location"], *self.collision_box["size"]]):
                    self.state_up = False
                    break
            if self.state_up == True:
                for enemy in enemies: # Check if entity is pressing it
                    if collision([*enemy.collision_box["location"], *enemy.collision_box["size"]], [*self.collision_box["location"], *self.collision_box["size"]]):
                        self.state_up = False
                        break
    
    def save(self):
        data = {"id": 5,
                "colour": self.colour}
        return data
    
    def get_rendering_row(self):
        return self.y_pos
    
    def draw(self, screen):
        from classes.global_data import constants_structure;
        constants = constants_structure()
        
        # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface = pygame.Surface(constants.SQUARE_SIZE, pygame.SRCALPHA) 
        
        # Pick texture depending on state
        if self.state_up:
            temp_surface.blit(pygame.transform.scale(self.textures["up"], constants.SQUARE_SIZE),(0,0))
        else:
            temp_surface.blit(pygame.transform.scale(self.textures["down"], constants.SQUARE_SIZE),(0,0))
            
        # Apply texture
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        return screen