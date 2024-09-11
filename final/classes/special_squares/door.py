import pygame

class Door:
    def __init__(self, x, y, hinge_corner, starting_dir, room_location, door_type=""):
        # x and y are grid coordinates and wil be translated to screen coordinates
        
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Pre-calculate all coordinates
        self.grid_location = [x,y]
        x = (x * constants.SQUARE_SIZE[0]) + room_location[0]
        y = (y * constants.SQUARE_SIZE[1]) + room_location[1]
        self.starting_dir = starting_dir
        
        # state is either 'h' or 'v' (horizontal of vertical)
        self.state = starting_dir
        self.corner = hinge_corner
        self.is_open = False
        
        self.x_pos = x
        self.y_pos = y
        
        # Load both textures
        self.textures = {"h": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/{door_type}door_right.png").convert(), constants.SQUARE_SIZE),
                        "v": pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/squares/{door_type}door_up.png").convert(), (constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 2))}
        
        
        
        # Possible hinge corner values: bottom_left, bottom_right, top_left, top_right
        
        # Load both collision boxes
        self.collision_boxes = {
            "h": {"size": (constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 0.1),  "location": [x, y + (constants.SQUARE_SIZE[1] * 0.9)]},
            "v": {"size": (constants.SQUARE_SIZE[0] * 0.1, constants.SQUARE_SIZE[1]),  "location": [x, y]}
        }
        
        self.collision_box = self.collision_boxes[starting_dir]
        
        
        # Re-align textures and collision box according to door coordinate
        if hinge_corner == "bottom_right":
            self.collision_boxes["v"]["location"][0] = x + (constants.SQUARE_SIZE[0] * 0.9)
            self.textures["h"] = pygame.transform.flip(self.textures["h"], True, False)
            #self.textures["v"] = pygame.transform.flip(self.textures["v"], True, False)
            
            
        elif hinge_corner == "top_left":
            self.collision_boxes["h"]["location"][1] = y
            temp_surface = pygame.Surface((constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 2), pygame.SRCALPHA)
            temp_surface.blit(self.textures["h"], (0,0))
            self.textures["h"] = temp_surface
            
            
        elif hinge_corner == "top_right":
            self.collision_boxes["h"]["location"][1] = y
            self.collision_boxes["v"]["location"][0] = x + (constants.SQUARE_SIZE[0] * 0.9)
            self.textures["h"] = pygame.transform.flip(self.textures["h"], True, False)
            #self.textures["v"] = pygame.transform.flip(self.textures["v"], True, False)
            
            temp_surface = pygame.Surface((constants.SQUARE_SIZE[0], constants.SQUARE_SIZE[1] * 2), pygame.SRCALPHA)
            temp_surface.blit(self.textures["h"], (0,0))
            self.textures["h"] = temp_surface
            
        # Set default attributes (inheriting classes can edit these)
        self.manual = True
        self.type = "manual"
        
    def toggle_state(self): # Switches door position depending on current one
        self.is_open = not self.is_open
        if self.state == "v":
            self.state = "h"
            self.collision_box = self.collision_boxes["h"]
        else:
            self.state = "v"
            self.collision_box = self.collision_boxes["v"]
            
            
    def open(self): # Sets door to be open
        if self.starting_dir == self.state:
            self.is_open = True
            if self.state == "v":
                self.state = "h"
                self.collision_box = self.collision_boxes["h"]
            else:
                self.state = "v"
                self.collision_box = self.collision_boxes["v"]
    
    def close(self): # Sets door to be closed
        if self.starting_dir != self.state:
            self.is_open = False
            self.state = self.starting_dir
            self.collision_box = self.collision_boxes[self.starting_dir]
            
            
    def save(self):
        # Generate position string
        pos = self.state
        pos += self.corner[0]
        if "left" in self.corner:
            pos += "l"
        else:
            pos += "r"
            
        data = {"id": 3,
                "pos": pos}
        return data
    
    def get_rendering_row(self):
        return self.collision_box["location"][1]
        
    def draw(self, screen):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Draw for vertical state
        if self.state == 'v':
            temp_surface = pygame.Surface((self.textures["v"].get_width(), self.textures["v"].get_height()), pygame.SRCALPHA)
            temp_surface.blit(self.textures["v"], (0,0))
            if self.corner.find("right") != -1:
                screen.blit(temp_surface, (self.x_pos + (constants.SQUARE_SIZE[1] * 0.65), self.y_pos - constants.SQUARE_SIZE[1]))
            else:
                screen.blit(temp_surface, (self.x_pos - (constants.SQUARE_SIZE[1] * 0.15), self.y_pos - constants.SQUARE_SIZE[1]))
            
        # Draw for horizontal state
        elif self.state == 'h':
            temp_surface = pygame.Surface((self.textures["h"].get_width(), self.textures["h"].get_height()), pygame.SRCALPHA)
            temp_surface.blit(self.textures["h"], (0,0))
            if self.corner.find("top") != -1:
                screen.blit(temp_surface, (self.x_pos, self.y_pos - int(constants.SQUARE_SIZE[1] * 0.7)))
            else:
                screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        return screen
