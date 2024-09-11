
from classes.entity import Entity
from classes.global_data import constants_structure

import pygame


class Crate(Entity):
    def __init__(self, x, y, room_loc):
        # x and y are grid locations, not coordinates (they will be translated shortly)
        constants = constants_structure()
        self.texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/entities/crate.png").convert(), constants.SQUARE_SIZE)
        
        
        self.x_pos = (x * constants.SQUARE_SIZE[0]) + room_loc[0]
        self.y_pos = (y * constants.SQUARE_SIZE[1])+ room_loc[1]
        self.width = constants.SQUARE_SIZE[0]
        self.height = constants.SQUARE_SIZE[1]
        self.size = [self.width, self.height]
        
        self.collision_box = {"location": [self.x_pos + (self.width * 0.05), self.y_pos + (self.height //2)],
                                "size": [constants.SQUARE_SIZE[0] * 0.9, constants.SQUARE_SIZE[1]//2]}
        #self.collision_box = {"location": [self.x_pos, self.y_pos],
        #                    "size": constants.SQUARE_SIZE}
        
        
    def move(self, direction, speed, room, crates, doors, entities, moved_crates = []):
        from functions.algorithms.collision_detection import is_colliding, collision
        constants = constants_structure()
        # must check if move can be done, and then carry it out. wether it can and has been done should be returned to the player
        
        # Will not push item right to edge, due to only moving at speed. 
        # Maybe implement system sothat if there is a collision, it checks 
        # every distance it could move between 1 and the speed so that it 
        # goes right to the edge. This will help with squeezing through thin gaps
        
        # self.collision_box = {"location": [self.x_pos, self.y_pos],
        #                 "size": constants.SQUARE_SIZE}
        moved_crates.append(self)
        
        
        if direction == "left":
            self.collision_box["location"][0] -= speed
        elif direction == "right":
            self.collision_box["location"][0] += speed
        elif direction == "up":
            self.collision_box["location"][1] -= speed
        elif direction == "down":
            self.collision_box["location"][1] += speed
        
        colliding = is_colliding(self.collision_box, room.layout, room.location, constants.SQUARE_SIZE)
        # MAKE PUSH ALGORITHM CHAINABLE
        if not colliding:
            for crate in crates:
                if not crate in moved_crates:
                    if collision([*self.collision_box["location"], *self.collision_box["size"]], 
                                [*crate.collision_box["location"], *crate.collision_box["size"]]):
                        if not crate.move(direction, speed, room, crates, entities, moved_crates):
                            colliding = True
            
            if not colliding:
                for door in doors:
                    if collision([*self.collision_box["location"], *self.collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                        colliding = True
                            
            if not colliding:
                for entity in entities:
                    if collision([*self.collision_box["location"], *self.collision_box["size"]], 
                                    [*entity.collision_box["location"], *entity.collision_box["size"]]):
                        if not entity.push(direction, speed, room, crates, doors):
                            colliding = True
            # If still not colliding, carry out movement
            if not colliding:
                self.x_pos = self.collision_box["location"][0] - (self.width * 0.05)
                self.y_pos = self.collision_box["location"][1] - (self.height //2)
            
        self.collision_box = {"location": [self.x_pos + (self.width * 0.05), self.y_pos + (self.height //2)],
                                "size": [constants.SQUARE_SIZE[0] * 0.9, constants.SQUARE_SIZE[1]//2]}
        
        return not colliding # can move
        
    
    def save(self, room_loc):
        constants = constants_structure()
        
        data = {
            "name": "crate",
            "x": (self.x_pos - room_loc[0]) / constants.SQUARE_SIZE[0],
            "y": (self.y_pos - room_loc[1]) / constants.SQUARE_SIZE[1]
        }
        
        return data
    
    def get_rendering_row(self):
        return self.collision_box["location"][1]
        
    def draw(self, screen):
        temp_surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(pygame.transform.scale(self.texture, [self.width, self.height]),(0,0))
        
        # collision box
        # pygame.draw.rect(temp_surface, (255, 0, 0, 127), (self.collision_box["location"][0] - self.x_pos, self.collision_box["location"][1] - self.y_pos, *self.collision_box["size"]))
        
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        return screen