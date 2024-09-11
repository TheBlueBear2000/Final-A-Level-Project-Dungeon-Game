import pygame
from functions.algorithms.collision_detection import is_colliding

class LivingItem:
    def __init__(self, x, y, item, velocity=[0,0]):
        self.item = item
        
        self.x_pos = x
        self.y_pos = y
        self.size = (40,40)
        self.velocity = velocity
        # hitbox is the same width but only the bottom half of height. This is derived from location and size when required
        
        
    def move(self, room_layout, room_location, constants):
        DECELERATION = 1
        
        hitbox = {"size": [self.size[0],self.size[1]//2],
                            "location": [self.x_pos,self.y_pos]}
        
        # Check collisions for X and Y movement
        if not is_colliding({"size": [self.size[0],self.size[1]//2],
                            "location": [self.x_pos + self.velocity[0], self.y_pos]}, 
                            room_layout, room_location, constants.SQUARE_SIZE):
            self.x_pos += self.velocity[0]
        if not is_colliding({"size": [self.size[0],self.size[1]//2],
                            "location": [self.x_pos, self.y_pos + self.velocity[1]]}, 
                            room_layout, room_location, constants.SQUARE_SIZE):
            self.y_pos += self.velocity[1]
        
        # Tend velocity towards 0 for X and Y
        if self.velocity[0] < 0:
            self.velocity[0] += DECELERATION
        elif self.velocity[0] > 0:
            self.velocity[0] -= DECELERATION
        
        if self.velocity[1] < 0:
            self.velocity[1] += DECELERATION
        elif self.velocity[1] > 0:
            self.velocity[1] -= DECELERATION
            
    def save(self, room_loc):
        
        data = {
            "name": "item",
            "x": self.x_pos,
            "y": self.y_pos,
            "item": self.item.type,
            "payload": self.item.payload
        }
        
        return data
    
    def get_rendering_row(self):
        return self.y_pos
        
    def draw(self, screen):
        temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        # Shadow (create translucent rectangle)
        pygame.draw.rect(temp_surface, (0, 0, 0, 128), (0, self.size[1]//8*7, self.size[0], self.size[1]//8))
        # Texture
        temp_surface.blit(pygame.transform.scale(self.item.game_texture, self.size), (0,0))
        
        # Apply to screen
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        return screen
    