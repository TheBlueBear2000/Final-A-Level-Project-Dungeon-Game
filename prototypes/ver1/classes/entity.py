

import pygame
from functions.algorithms.aoeScanner import aoeScanner

class Entity:
    def __init__(self, x, y, type, room_loc, drops):
        # Constants
        from classes.global_data import constants_structure
        constants = constants_structure()

        self.initiate_assets(type, constants)
        
        self.type = type
        self.state = "idle"
        self.direction = "down"
        
        self.x_pos = (x * constants.SQUARE_SIZE[0]) + room_loc[0] - 50
        self.y_pos = (y * constants.SQUARE_SIZE[1]) + room_loc[1] - 60
        #print(x, y)
        #print(self.x_pos, self.y_pos)
        
        self.movement_vector = [0,0]
        self.speed = 2
        self.size = (150,150)
        self.animation_frame_time = 0.1
        self.animation_cooldown = 0
        self.max_health = 5
        self.health = self.max_health
        self.mele_reach = 60
        self.attack_damage = 3
        self.attack_timer = 0
        self.team = None
        
        # path is an array of coordinates that lead to a destination, allowing navigation around corners
        #self.path = []
        
        
        self.collision_box = {"size": (48, 25),
                            "location": [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 40 + self.y_pos]}
        
        self.get_square = lambda room : [int((self.collision_box["location"][0] - room.location[0])//constants.SQUARE_SIZE[0]),
                                        int((self.collision_box["location"][1] - room.location[1])//constants.SQUARE_SIZE[1])]
        
        # possible states: idle, run, sprint, boost, push, pull, attack, take_damage, death, fall
        self.change_state("spawn")
        
        self.drops = self.calculate_drops(drops)
        
        
    def move(self, destination, room_data, crates, doors, forced = False):
        # path can either be algorithmic path to player, or path to random local location if entity is idle
        # CALCULATE MOVEMENT VECTOR
        if not forced:
            from functions.algorithms.getMovementVector import get_movement_vector
            self.movement_vector = get_movement_vector(self.speed, [destination[0] - self.collision_box["location"][0],  destination[1] - self.collision_box["location"][1]])
        else:
            self.movement_vector = destination
        # movement vector will be next travel coordinate
        # if [self.x_pos, self.y_pos] == self.path[0]:
        #     self.path.pop(0)
            
        # if self.path != []:
        #     from functions.algorithms.getMovementVector import get_movement_vector
        #     self.movement_vector = get_movement_vector(self.speed, self.path[0]) # destination is the 0th item of the path
        
        from functions.algorithms.collision_detection import is_colliding, collision
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        can_move = [False, False]
        self.collision_box["location"] = [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos]
        
        
        
        # X
        projected_collision_box = {
            "size": self.collision_box["size"],
            "location": [self.collision_box["location"][0] + self.movement_vector[0], self.collision_box["location"][1]]
        }
        
        if not is_colliding(projected_collision_box, room_data.layout, room_data.location, constants.SQUARE_SIZE):
            can_move[0] = True
            
        for door in doors:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                can_move[0] = False
                
        for crate in crates:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*crate.collision_box["location"], *crate.collision_box["size"]]):
                can_move[0] = False
                break
            
            
        # Y
        projected_collision_box = {
            "size": self.collision_box["size"],
            "location": [self.collision_box["location"][0], self.collision_box["location"][1] + self.movement_vector[1]]
        }
        if not is_colliding(projected_collision_box, room_data.layout, room_data.location, constants.SQUARE_SIZE):
            can_move[1] = True
        
        for door in doors:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                can_move[1] = False
                
        for crate in crates:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*crate.collision_box["location"], *crate.collision_box["size"]]):
                can_move[1] = False
                break
        
        if can_move[0] and can_move[1]:
            self.x_pos += self.movement_vector[0]
            self.y_pos += self.movement_vector[1]
        elif can_move[0]:
            self.x_pos += (self.movement_vector[0]//abs(self.movement_vector[0])) * self.speed
        elif can_move[1]:
            self.y_pos += (self.movement_vector[1]//abs(self.movement_vector[1])) * self.speed
        
        # calculate animation state change
        #print(self.movement_vector)
        #if self.state in ["idle", "run"]: # check that the state shouldnt be anything else
        if self.movement_vector == [0,0] and not self.state == "idle":
            self.change_state("idle")
        elif self.movement_vector != [0,0] and not self.state == "run":
            self.change_state("run") # check for running state (called "run"
                
        self.check_direction()
                
        self.collision_box["location"] = [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos]
        
    def push(self, direction, speed, room, crates, doors):
        from functions.algorithms.collision_detection import is_colliding, collision
        from classes.global_data import constants_structure
        constants = constants_structure()
        # must check if move can be done, and then carry it out. wether it can and has been done should be returned to the player
        
        # Will not push item right to edge, due to only moving at speed. 
        # Maybe implement system sothat if there is a collision, it checks 
        # every distance it could move between 1 and the speed so that it 
        # goes right to the edge. This will help with squeezing through thin gaps
        
        # self.collision_box = {"location": [self.x_pos, self.y_pos],
        #                 "size": constants.SQUARE_SIZE}
        
        if direction == "left":
            self.collision_box["location"][0] -= speed
        elif direction == "right":
            self.collision_box["location"][0] += speed
        elif direction == "up":
            self.collision_box["location"][1] -= speed
        elif direction == "down":
            self.collision_box["location"][1] += speed
        
        colliding = is_colliding(self.collision_box, room.layout, room.location, constants.SQUARE_SIZE)
        
        # Doors
        if not colliding:
            for door in doors:
                if collision([*self.collision_box["location"], *self.collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                    colliding = True
                    break
        
        # Crates
        if not colliding:
            hit_crate = False
            for crate in crates:
                if collision([*self.collision_box["location"], *self.collision_box["size"]], 
                            [*crate.collision_box["location"], *crate.collision_box["size"]]):
                    hit_crate = True
                    colliding = True
                    # if crate.move(direction, speed, room, crates, moved_crates):
                    #     self.x_pos = self.collision_box["location"][0] - (self.width * 0.05)
                    #     self.y_pos = self.collision_box["location"][1] - (self.height //2)
                    # else: 
                    #     colliding = True
            if not hit_crate:
                if direction == "left" or direction == "right":
                    self.x_pos += speed * (-1 if direction == "left" else 1)
                else:
                    self.y_pos += speed * (-1 if direction == "up" else 1)
            
        self.collision_box["location"] = [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos]
        
        return not colliding # can move
    
    def change_state(self, new_state):
        self.state = new_state
        self.animation_frame = 0
    
    def check_direction(self):
        if self.movement_vector != [0,0]:
            if self.movement_vector[0] == 0:
                if self.movement_vector[1] < 0:
                    self.direction = "up"
                else:
                    self.direction = "down"
            if self.movement_vector[0] < 0:
                self.direction = "left"
            elif self.movement_vector[0] > 0:
                self.direction = "right"
                
                
    def attack(self, player, entities, room):
        from functions.algorithms.getMovementVector import get_movement_vector
        from classes.global_data import constants_structure
        constants = constants_structure()
        self.change_state("attack")
        self.attack_timer = 3
        
        range_vector = get_movement_vector(self.mele_reach, self.movement_vector)
        attack_loc = [(self.collision_box["location"][0] + (self.collision_box["size"][0]//2)) + range_vector[0],
                        (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)) + range_vector[1]]
        effectedEntities, effectedSquares, playerEffected = aoeScanner(attack_loc, entities, room, player, self.mele_reach, constants)
        
        # player
        if playerEffected and (self.team != player.team):
            player.take_damage(self.attack_damage)
        # entities
        for entity in effectedEntities:
            if entity.team != self.team:
                entity.take_damage(self.attack_damage)
        
    def take_damage(self, damage):
        self.change_state("take_damage")
        self.health -= damage
        if self.health <= 0:
            self.die()
            return True, self.drops
        return False, []
            
    def die(self):
        if self.state != "death":
            self.change_state("death")
            
    def calculate_drops(self, drops):
        from random import randint
        out_drops = []
        for set in drops: # for every seperate set of rolls
            set_drops = []
            for item in set["drops"]:
                for instance in range(item["chance"]):
                    payload = {}
                    if "payload" in item:
                        payload = item["payload"]
                    set_drops.append({"item": item["item"], "payload": payload}) # makes one long array with all possible choices
                    
            while len(set_drops) < set["total"]:
                set_drops.append(None) # complete list to length
                    
            for roll in range(set["rolls"]):
                out_drops.append(set_drops[randint(0, set["total"]-1)])
        return out_drops
            
            
    def save(self, room_loc):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        data = {
            "name": self.type,
            "x": (self.x_pos + 50 - room_loc[0]) / constants.SQUARE_SIZE[0],
            "y": (self.y_pos + 60 - room_loc[1]) / constants.SQUARE_SIZE[1],
            "health": self.health
            }
        return data

    
        #self.x_pos = (x * constants.SQUARE_SIZE[0]) + room_loc[0] - 50
        #self.y_pos = (y * constants.SQUARE_SIZE[1]) + room_loc[1] - 60
        
    def get_rendering_row(self):
        return self.collision_box["location"][1]
        
    def draw(self, screen):
        
        #pygame.draw.rect(screen, (0, 0, 0), (self.x_pos, self.y_pos, 10,10))
        
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        FPS = constants.MENU_FPS * 2
        
        if (self.state == "idle" or
            self.state == "run" or
            self.state == "push" or
            self.state == "pull" or
            self.state == "attack"):
            animation = self.state + "_" + self.direction
            
        else:
            animation = self.state
            
        
        self.chosen_asset = self.assets[animation][self.animation_frame]
        
        temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(pygame.transform.scale(self.chosen_asset, self.size),(0,0))
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        self.animation_cooldown += 1
    
        if self.animation_cooldown >= FPS // (1/self.animation_frame_time):
            self.animation_cooldown = 0
            self.animation_frame += 1
            
        
        if self.animation_frame == len(self.assets[animation]):
            self.animation_frame = 0
        
        
        # DRAW COLLISON BOX:
        # temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        # pygame.draw.rect(temp_surface, (255, 0, 0, 127), (0, 0, *self.collision_box["size"]))
        # screen.blit(temp_surface, self.collision_box["location"])
        
        
        # Draw details
        # Health bar
        if self.health != self.max_health:
            health_bar_location = [self.collision_box["location"][0] + (self.collision_box["size"][0]//2), self.collision_box["location"][1] + self.collision_box["size"][1] + 10]
            health_bar_size = [self.collision_box["size"][0], 5]
            # Black background
            pygame.draw.rect(screen, (0, 0, 0), (health_bar_location[0] - (health_bar_size[0]//2), health_bar_location[1] - health_bar_size[1] - 10, *health_bar_size))
            # Green fill
            bar_width = int(health_bar_size[0] * self.health / self.max_health)
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_location[0] - (health_bar_size[0]//2), health_bar_location[1] - health_bar_size[1] - 10, 
                                                    bar_width, health_bar_size[1]))
        
        
        return screen
    
    def initiate_assets(self, type, constants):
        self.assets = {}
        #with open(constants.FILE_PATH + "project_lib/assets/player/main.png", 'r') as asset_file:
        
        
        master_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/entities/{type}.png").convert() # Use text input button design
        images = []
        for row in range(master_texture.get_height()//48):
            row_textures = []
            for image in range(master_texture.get_width()//48):
                texture_surface = pygame.Surface((48, 48))
                texture_surface.blit(master_texture, (0, 0), (48*image, 48*row, 48, 48))
                row_textures.append(texture_surface)
            images.append(row_textures)
            
        # Existing assets
        self.assets["idle_up"] = images[1][:8]
        self.assets["idle_down"] = images[0][:8]
        self.assets["run_up"] = images[3][:6]
        self.assets["run_down"] = images[2][:6]
        
        self.assets["attack_right"] = images[2][6:9]
        self.assets["attack_down"] = images[3][6:9]
        self.assets["attack_up"] = images[4][6:9]
        
        self.assets["push_right"] = images[4][:6]
        self.assets["pull_left"] = images[5][:6]
        
        self.assets["take_damage"] = images[5][6:9]
        
        self.assets["push_up"] = images[6][:4]
        self.assets["pull_up"] = images[7][:4]
        self.assets["pull_down"] = images[6][4:9]
        self.assets["push_down"] = images[7][4:9]
        
        self.assets["death"] = images[8][:5]
        self.assets["fall"] = images[9][:5]
        
        # Derived assets
        
        self.assets["idle_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["idle_down"]] # this line of code returns a flipped version of every frame of the animation
        self.assets["run_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["run_down"]]
        self.assets["attack_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["attack_right"]]
        self.assets["push_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["push_right"]]
        
        self.assets["idle_right"] = self.assets["idle_down"]
        self.assets["run_right"] = self.assets["run_down"]
        self.assets["pull_right"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["pull_left"]]

        self.assets["spawn"] = images[8][:5]
        self.assets["spawn"].reverse()
        # DRAW BOOST ANIMATION