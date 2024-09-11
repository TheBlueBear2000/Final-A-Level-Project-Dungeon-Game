import pygame
from functions.algorithms.aoeScanner import aoeScanner

class Entity:
    def __init__(self, x, y, type, room_loc, drops):
        # Constants
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Set attributes

        self.initiate_assets(type, constants)
        
        self.type = type
        self.state = "idle"
        self.direction = "down"
        
        # Calculate screen coordinates from grid coordinates
        self.x_pos = (x * constants.SQUARE_SIZE[0]) + room_loc[0] - 50
        self.y_pos = (y * constants.SQUARE_SIZE[1]) + room_loc[1] - 60
        
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
        
        
        self.collision_box = {"size": (48, 25),
                            "location": [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 40 + self.y_pos]}
        
        # Turns screen coordinates back to grid coordinates when necessary
        self.get_square = lambda room : [int((self.collision_box["location"][0] - room.location[0])//constants.SQUARE_SIZE[0]),
                                        int((self.collision_box["location"][1] - room.location[1])//constants.SQUARE_SIZE[1])]
        
        # possible states: idle, run, sprint, boost, push, pull, attack, take_damage, death, fall
        self.change_state("spawn")
        
        # Precalculate entity drops to save memory
        self.drops = self.calculate_drops(drops)
        
        
    def move(self, destination, room_data, crates, doors, forced = False):
        # Path can either be algorithmic path to player, or path to random local location if entity is idle
        # CALCULATE MOVEMENT VECTOR
        if not forced:
            # Find vector of entity speed going towards destination
            from functions.algorithms.getMovementVector import get_movement_vector
            self.movement_vector = get_movement_vector(self.speed, [destination[0] - self.collision_box["location"][0],  destination[1] - self.collision_box["location"][1]])
        else:
            # Teleports entity to destination if necessary
            self.movement_vector = destination
            
        from functions.algorithms.collision_detection import is_colliding, collision
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        can_move = [False, False]
        self.collision_box["location"] = [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos]
        
        
        # Do all X checks
        projected_collision_box = {
            "size": self.collision_box["size"],
            "location": [self.collision_box["location"][0] + self.movement_vector[0], self.collision_box["location"][1]]
        }
        
        # Check squares
        if not is_colliding(projected_collision_box, room_data.layout, room_data.location, constants.SQUARE_SIZE):
            can_move[0] = True
            
        # Check doors
        for door in doors:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                can_move[0] = False
        
        # Check crates
        for crate in crates:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*crate.collision_box["location"], *crate.collision_box["size"]]):
                can_move[0] = False
                break
            
            
        # Do all Y checks
        projected_collision_box = {
            "size": self.collision_box["size"],
            "location": [self.collision_box["location"][0], self.collision_box["location"][1] + self.movement_vector[1]]
        }
        
        # Check squares
        if not is_colliding(projected_collision_box, room_data.layout, room_data.location, constants.SQUARE_SIZE):
            can_move[1] = True
        
        # Check doors
        for door in doors:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                can_move[1] = False
                
        # Check crates
        for crate in crates:
            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*crate.collision_box["location"], *crate.collision_box["size"]]):
                can_move[1] = False
                break
        
        # Do possible movements
        if can_move[0] and can_move[1]:
            self.x_pos += self.movement_vector[0]
            self.y_pos += self.movement_vector[1]
        
        # If only one direction is possible, walk in that direction at normal speed so that entity 
        # doesn't look like it is rubbing on wall. Makes movement look more intentional.
        elif can_move[0]: 
            self.x_pos += (self.movement_vector[0]//abs(self.movement_vector[0])) * self.speed
        elif can_move[1]:
            self.y_pos += (self.movement_vector[1]//abs(self.movement_vector[1])) * self.speed
        
        # calculate animation state change
        if self.movement_vector == [0,0] and not self.state == "idle":
            self.change_state("idle")
        elif self.movement_vector != [0,0] and not self.state == "run":
            self.change_state("run")
                
        self.check_direction()
                
        # Update collision box
        self.collision_box["location"] = [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos]
        
    def push(self, direction, speed, room, crates, doors):
        # Very similar to crate pushing function
        from functions.algorithms.collision_detection import is_colliding, collision
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Pre-make move
        if direction == "left":
            self.collision_box["location"][0] -= speed
        elif direction == "right":
            self.collision_box["location"][0] += speed
        elif direction == "up":
            self.collision_box["location"][1] -= speed
        elif direction == "down":
            self.collision_box["location"][1] += speed
        
        # Check square collisions
        colliding = is_colliding(self.collision_box, room.layout, room.location, constants.SQUARE_SIZE)
        
        # Check door collisions
        if not colliding:
            for door in doors:
                if collision([*self.collision_box["location"], *self.collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                    colliding = True
                    break
        
        # Check crate collisions
        if not colliding:
            hit_crate = False
            for crate in crates:
                if collision([*self.collision_box["location"], *self.collision_box["size"]], 
                            [*crate.collision_box["location"], *crate.collision_box["size"]]):
                    hit_crate = True
                    colliding = True
                    
            # Update movement
            if not hit_crate:
                if direction == "left" or direction == "right":
                    self.x_pos += speed * (-1 if direction == "left" else 1)
                else:
                    self.y_pos += speed * (-1 if direction == "up" else 1)
            
        # Update collision box
        self.collision_box["location"] = [(self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos]
        
        return not colliding # can move
    
    def change_state(self, new_state):
        # Set state to new state, as well as resetting animation frame so that animation starts from start
        self.state = new_state
        self.animation_frame = 0
    
    def check_direction(self):
        # Calculates direction based on movement vector
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
        
        # Initiate attack animation
        self.change_state("attack")
        self.attack_timer = 3
        
        # Calculate lists of all effected squares and entities based on attack range
        range_vector = get_movement_vector(self.mele_reach, self.movement_vector)
        attack_loc = [(self.collision_box["location"][0] + (self.collision_box["size"][0]//2)) + range_vector[0],
                        (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)) + range_vector[1]]
        effectedEntities, effectedSquares, playerEffected = aoeScanner(attack_loc, entities, room, player, self.mele_reach, constants)
        
        
        # Attack player if player effected
        if playerEffected and (self.team != player.team):
            player.take_damage(self.attack_damage)
            
        # Attack entities if they are effected
        for entity in effectedEntities:
            if entity.team != self.team:
                entity.take_damage(self.attack_damage)
        
    def take_damage(self, damage):
        # Set animation
        self.change_state("take_damage")
        # Reduce health and check for deaths
        self.health -= damage
        if self.health <= 0:
            self.die()
            return True, self.drops # If died, tell player so that object can be removed from list and killed. Also return drops
        return False, []
            
    def die(self):
        # Start dying animation
        if self.state != "death":
            self.change_state("death")
            
    def calculate_drops(self, drops):
        from random import randint
        out_drops = []
        for set in drops: # for every seperate set of rolls
            set_drops = []
            for item in set["drops"]: # Go through each item in that set
                for instance in range(item["chance"]):
                    payload = {}
                    if "payload" in item:
                        payload = item["payload"]
                    set_drops.append({"item": item["item"], "payload": payload}) # makes one long array with all possible choices according to weights
                    
            while len(set_drops) < set["total"]:
                set_drops.append(None) # complete list with empty drops to complete length
                    
            for roll in range(set["rolls"]):
                # For each roll of each set, add a random item from full drops list.
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
        
    def get_rendering_row(self):
        return self.collision_box["location"][1]
        
    def draw(self, screen):
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        FPS = constants.MENU_FPS * 2
        
        if (self.state == "idle" or
            self.state == "run" or
            self.state == "push" or
            self.state == "pull" or
            self.state == "attack"):
            # Get animation name for directional animations
            animation = self.state + "_" + self.direction
            
        else:
            # Get animation name for non-directional animations
            animation = self.state
            
        
        # Choose asset based on animation and current frame
        self.chosen_asset = self.assets[animation][self.animation_frame]
        
        # Draw asset to screen
        temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(pygame.transform.scale(self.chosen_asset, self.size),(0,0))
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        
        # Update animation frame
        self.animation_cooldown += 1
    
        if self.animation_cooldown >= FPS // (1/self.animation_frame_time):
            self.animation_cooldown = 0
            self.animation_frame += 1
        
        if self.animation_frame == len(self.assets[animation]):
            self.animation_frame = 0
        
        
        # Code to draw collision box for development purposes:
        # temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        # pygame.draw.rect(temp_surface, (255, 0, 0, 127), (0, 0, *self.collision_box["size"]))
        # screen.blit(temp_surface, self.collision_box["location"])
        
        
        # Draw health bar if necessary
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
        
        # Get sprite-sheet
        master_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/entities/{type}.png").convert() # Use text input button design
        images = []
        
        # Extract each seperate image from sprite sheet into 2D array
        for row in range(master_texture.get_height()//48):
            row_textures = []
            for image in range(master_texture.get_width()//48):
                texture_surface = pygame.Surface((48, 48))
                texture_surface.blit(master_texture, (0, 0), (48*image, 48*row, 48, 48))
                row_textures.append(texture_surface)
            images.append(row_textures)
            
            
        # Extract animations manually from images array

        # Direct animations
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
        
        # Animations derived from existing ones
        self.assets["idle_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["idle_down"]] # this line of code returns a flipped version of every frame of the animation
        self.assets["run_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["run_down"]]
        self.assets["attack_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["attack_right"]]
        self.assets["push_left"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["push_right"]]
        
        self.assets["idle_right"] = self.assets["idle_down"]
        self.assets["run_right"] = self.assets["run_down"]
        self.assets["pull_right"] = [pygame.transform.flip(texture, True, False) for texture in self.assets["pull_left"]]

        self.assets["spawn"] = images[8][:5]
        self.assets["spawn"].reverse()
        
        # SPACE FOR MORE ANIMATIONS IF NEEDED
