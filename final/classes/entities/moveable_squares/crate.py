from classes.entity import Entity
from classes.global_data import constants_structure
import pygame

class Crate(Entity): # The Crate class extends the Entity class
    def __init__(self, x, y, room_loc):
        # x and y parameters are grid locations, not screen coordinates (they will be translated to screen coordinates)
        constants = constants_structure()
        self.texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/entities/crate.png").convert(), constants.SQUARE_SIZE)
        
        # Pre-calculate all coordinates
        self.x_pos = (x * constants.SQUARE_SIZE[0]) + room_loc[0]
        self.y_pos = (y * constants.SQUARE_SIZE[1])+ room_loc[1]
        self.width = constants.SQUARE_SIZE[0]
        self.height = constants.SQUARE_SIZE[1]
        self.size = [self.width, self.height]
        
        self.collision_box = {"location": [self.x_pos + (self.width * 0.05), self.y_pos + (self.height //2)],
                                "size": [constants.SQUARE_SIZE[0] * 0.9, constants.SQUARE_SIZE[1]//2]}
        
        
    def move(self, direction, speed, room, crates, doors, entities, moved_crates = []):
        from functions.algorithms.collision_detection import is_colliding, collision
        constants = constants_structure()
        # Checks if move can be done, and then carries it out. Whether it can and has been done is returned to the player
        
        moved_crates.append(self)
        
        # Do movement
        if direction == "left":
            self.collision_box["location"][0] -= speed
        elif direction == "right":
            self.collision_box["location"][0] += speed
        elif direction == "up":
            self.collision_box["location"][1] -= speed
        elif direction == "down":
            self.collision_box["location"][1] += speed
        
        # Check if the crate is colliding with any squares
        colliding = is_colliding(self.collision_box, room.layout, room.location, constants.SQUARE_SIZE)
        
        # If not, check other squares and entities to see if they are colliding
        if not colliding:
            for crate in crates: # Check other crates
                if not crate in moved_crates:
                    if collision([*self.collision_box["location"], *self.collision_box["size"]], 
                                [*crate.collision_box["location"], *crate.collision_box["size"]]):
                        if not crate.move(direction, speed, room, crates, entities, moved_crates): 
                            # Recursively checks other crates to check if they can be pushed. Will only not push if the chain is blocked
                            colliding = True
            
            if not colliding:
                for door in doors: # Check doors
                    if collision([*self.collision_box["location"], *self.collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                        colliding = True
                            
            if not colliding:
                for entity in entities: # Check entities
                    if collision([*self.collision_box["location"], *self.collision_box["size"]], 
                                    [*entity.collision_box["location"], *entity.collision_box["size"]]):
                        if not entity.push(direction, speed, room, crates, doors):
                            # Checks if entities can be added to push chain
                            colliding = True
                            
            # If still not colliding, carry out movement
            if not colliding:
                self.x_pos = self.collision_box["location"][0] - (self.width * 0.05)
                self.y_pos = self.collision_box["location"][1] - (self.height //2)
            
        # Update collision box
        self.collision_box = {"location": [self.x_pos + (self.width * 0.05), self.y_pos + (self.height //2)],
                                "size": [constants.SQUARE_SIZE[0] * 0.9, constants.SQUARE_SIZE[1]//2]}
        
        return not colliding # can move
        
    
    def save(self, room_loc):
        constants = constants_structure()
        # Collect important data
        data = {
            "name": "crate",
            "x": (self.x_pos - room_loc[0]) / constants.SQUARE_SIZE[0],
            "y": (self.y_pos - room_loc[1]) / constants.SQUARE_SIZE[1]
        }
        
        return data
    
    def get_rendering_row(self):
        return self.collision_box["location"][1]
        
    def draw(self, screen):
        # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA) 
        temp_surface.blit(pygame.transform.scale(self.texture, [self.width, self.height]),(0,0))
        
        # Code to show collision box (for development purposes):
        # pygame.draw.rect(temp_surface, (255, 0, 0, 127), (self.collision_box["location"][0] - self.x_pos, self.collision_box["location"][1] - self.y_pos, *self.collision_box["size"]))
        
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        return screen