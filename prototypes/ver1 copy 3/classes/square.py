import copy
import pygame

class Square:
    def __init__(self, square, default, file_path, square_size, location, grid_loc):
        self.data = copy.deepcopy(default)
        for data in square:
            self.data[data] = square[data]
        
        
        from classes.global_data import constants_structure
        constants = constants_structure()
    
        self.collidable = self.data["collidable"]
        self.breakable = self.data["breakable"]
        self.health = self.data["strength"]
        
        self.grid_loc = grid_loc
        
        self.location = location
        self.x_pos = location[0]
        self.width = self.data["collision_size"][0] * constants.SQUARE_SIZE[0]
        self.y_pos = location[1]
        self.height = self.data["collision_size"][1] * constants.SQUARE_SIZE[0]
        
        texture_names = self.data["textures"]
        self.textures = [pygame.transform.scale(pygame.image.load(file_path + f"project_lib/assets/squares/{texture_name}.png").convert(), square_size) for texture_name in texture_names]
            

    def draw(self, screen, x_loc, y_loc):
        temp_surface = pygame.Surface([self.textures[0].get_width(), self.textures[0].get_height()], pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(self.textures[0],(0,0))
        screen.blit(temp_surface, (x_loc, y_loc))
        
        #screen.blit(self.textures[0], (x_loc, y_loc)) # only doing 0 for now, since there are no animations yet
        return screen
    
    def calculate_drops(self):
        from random import randint
        drops = []
        for set in self.data["drops"]: # for every seperate set of rolls
            set_drops = []
            for item in set["drops"]:
                for instance in range(item["chance"]):
                    set_drops.append(item["item"]) # makes one long array with all possible choices
            while len(set_drops) < set["total"]:
                set_drops.append(None) # complete list to length
                    
            for roll in range(set["rolls"]):
                drops.append(set_drops[randint(0, set["total"]-1)])
        
        print("Drops: ", drops)
        return drops
    
    def take_damage(self, damage, room):
        self.health -= damage
        drops = []
        if self.health <= 0:
            drops = self.destroy(room)
        return drops
    
    def destroy(self, room):
        import json
        from classes.square import Square
        from classes.global_data import constants_structure
        constants = constants_structure()
        squares_data = json.load(open(constants.FILE_PATH + "data/squares/squares_data.json", "r"))
        default_square = json.load(open(constants.FILE_PATH + "data/squares/default_square.json", "r"))
        
        drops = []
        # sort drops
        if self.data["has_drops"]:
            drops = self.calculate_drops()
        
        # do break
        room.layout[self.grid_loc[1]][self.grid_loc[0]] = Square(squares_data[0], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, self.location, self.grid_loc)
        
        return drops