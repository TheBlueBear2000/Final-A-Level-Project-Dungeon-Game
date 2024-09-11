import pygame
from functions.algorithms.aoeScanner import aoeScanner

class Player:
    def __init__(self, x, y):
        # Constants
        from classes.global_data import constants_structure
        constants = constants_structure()

        self.initiate_assets(constants)
        
        self.state = "idle"
        self.direction = "down"
        
        self.max_health = 30
        self.health = self.max_health
        self.x_pos = x
        self.y_pos = y
        self.movement_vector = [0,0]
        self.speed = 6
        self.size = (150,150)
        self.sprinting = False
        self.sprint_multiplier = 2
        self.max_sprint_stamina = 45
        self.sprint_stamina = self.max_sprint_stamina
        self.max_boost_time = 75
        self.boost_cooldown = self.max_boost_time
        self.boost_frame = 0
        self.boost_speed = 8
        self.animation_frame_time = 0.1
        self.animation_cooldown = 0
        
        self.mele_reach = 50
        self.mele_push_strength = 30
        self.attack_damage = 1
        self.attack_timer = 0
        self.max_attack_cooldown = 5
        self.attack_cooldown = self.max_attack_cooldown
        
        self.team = "player"
        
        self.held_keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }
        
        self.collision_box = {"size": (48, 25),
                            "location": ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 40 + self.y_pos)}
        
        self.inventory = [None, None, # main and offhand 0-1
                        None, None, None, # Helmet, torso and legs 2-4
                        None, None, None, # Line one 5-7
                        None, None, None, # Line tw 8-10
                        None, None, None,] # Line three 11-13
        self.inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory.png").convert(), (constants.INV_ITEM_SIZE[0] * 3, constants.INV_ITEM_SIZE[1] * 5))
        self.selected_inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory_highlighted.png").convert(), constants.INV_ITEM_SIZE)
        self.holding_main_hand = True
        
        from classes.items.stick import StickSword
        self.inventory[0] = StickSword()
        
        # possible states: idle, run, sprint, boost, push, pull, attack, take_damage, death, fall
        self.change_state("idle")
        
        
    def move(self, key_bindings, events, room_data, entities, room, screen):
        
        if self.state == "death":
            if self.animation_frame == len(self.assets["death"])-1:
                return True
            else:
                return False

        
        
        if self.attack_cooldown < self.max_attack_cooldown:
            self.attack_cooldown += 1
        
        #if self.attack_timer > 0:
        #    self.attack_timer -= 1
            
        started_movements = []
        ended_movements = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) is not None: # key values are equal to the decimal ascii value of that key
                    started_movements.append(key_bindings[str(event.key)])
            if event.type == pygame.KEYUP:
                if key_bindings.get(str(event.key)) is not None: # key values are equal to the decimal ascii value of that key
                    ended_movements.append(key_bindings[str(event.key)])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if key_bindings.get("L_CLICK") is not None:
                    started_movements.append(key_bindings["L_CLICK"])
            if event.type == pygame.MOUSEBUTTONUP:
                if key_bindings.get("L_CLICK") is not None:
                    started_movements.append(key_bindings["L_CLICK"])
                    
                
        
        
        
        # Start togglable movements
        for movement in started_movements:
            if movement == "up":
                self.held_keys["up"] = True
            elif movement == "down":
                self.held_keys["down"] = True
            elif movement == "left":
                self.held_keys["left"] = True
            elif movement == "right":
                self.held_keys["right"] = True
                
            elif movement == "sprint":
                if self.sprint_stamina > 0:
                    self.sprinting = True
                    
            elif movement == "attack":
                if self.attack_cooldown == self.max_attack_cooldown:
                    self.attack_cooldown = 0
                    attack_damage = self.attack_damage # Default
                    # calculate from weapon
                    if self.holding_main_hand and (self.inventory[0] != None):
                        attack_damage = self.inventory[0].mele_damage
                    elif (not self.holding_main_hand) and (self.inventory[1] != None):
                        attack_damage = self.inventory[1].mele_damage
                        
                    self.attack(self, entities, room, attack_damage)
                
            # hand selection (boolean determines where in inventory array will be selected, since index 0 and 1 are the main and off hand respectively)
            elif movement == "switch_hand":
                self.holding_main_hand = not self.holding_main_hand
            elif movement == "main_hand":
                self.holding_main_hand = True
            elif movement == "off_hand":
                self.holding_main_hand = False
                
            # run screen buttons
            elif movement == "pause":
                from functions.loops.pause_screen import run as run_pause_screen
                run_pause_screen(screen, key_bindings)
            elif movement == "inventory":
                from functions.loops.inventory import run as open_inventory
                self.inventory = open_inventory(self.inventory, screen, key_bindings)
            # Boost functionality
            elif movement == "boost":
                if self.boost_cooldown == self.max_boost_time  and  (self.held_keys["up"] or self.held_keys["down"] or self.held_keys["left"] or self.held_keys["right"]):
                    self.boost_cooldown = 0
                    self.boost_frame = 3
                
        
        # end movements
        for movement in ended_movements:
            if movement == "up":
                self.held_keys["up"] = False
            elif movement == "down":
                self.held_keys["down"] = False
            elif movement == "left":
                self.held_keys["left"] = False
            elif movement == "right":
                self.held_keys["right"] = False
            elif movement == "sprint":
                self.sprinting = False
                
                
        multiplier = 1
        if self.sprinting:
            multiplier = self.sprint_multiplier
        
        # calculate vector
        self.movement_vector = [0,0]
        if self.held_keys["up"]:
            self.movement_vector[1] -= self.speed * multiplier
        if self.held_keys["down"]:
            self.movement_vector[1] += self.speed * multiplier
        if self.held_keys["left"]:
            self.movement_vector[0] -= self.speed * multiplier
        if self.held_keys["right"]:
            self.movement_vector[0] += self.speed * multiplier
        self.check_direction()
        
        
        # adjust stamina
        if self.sprinting and self.sprint_stamina > 0:
            self.sprint_stamina -= 1
        elif self.sprint_stamina < 45:
            self.sprint_stamina += 1
        
        if self.sprint_stamina == 0:
            self.sprinting = False
        
        # adjust boost cooldown
        if self.boost_cooldown < self.max_boost_time:
            self.boost_cooldown += 1
                    
                    
        moves = 1
        boosting = False
        if self.boost_frame > 0:
            boosting = True
            self.boost_frame -= 1
            moves = self.boost_speed
            
        # CALCULATE MOVEMENT VECTOR
        speed = self.speed # handle sprinting (replace later to account for pushing or non-sprinting states)
        if self.sprinting and not boosting:
            speed *= self.sprint_multiplier
        from functions.algorithms.getMovementVector import get_movement_vector
        self.movement_vector = get_movement_vector(speed, self.movement_vector)
        
        
        # DO ACTUAL MOVEMENT
        
        
        #if self.attack_timer == 0:
        from functions.algorithms.collision_detection import is_colliding
        from classes.global_data import constants_structure
        constants = constants_structure()
        for i in range(moves):
            self.collision_box["location"] = ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos)
            projected_collision_box = {
                "size": self.collision_box["size"],
                "location": (self.collision_box["location"][0] + self.movement_vector[0], self.collision_box["location"][1])
            }
            if not is_colliding(projected_collision_box, room_data["layout"], room_data["location"], constants.SQUARE_SIZE):
                self.x_pos += self.movement_vector[0]
                
            projected_collision_box = {
                "size": self.collision_box["size"],
                "location": (self.collision_box["location"][0], self.collision_box["location"][1] + self.movement_vector[1])
            }
            if not is_colliding(projected_collision_box, room_data["layout"], room_data["location"], constants.SQUARE_SIZE):
                self.y_pos += self.movement_vector[1]
            # CHANGE COLLISION BOX LOCATION TO BE PROJECTED LOCATION
        
        
        # calculate movement state change
        if self.state in ["idle", "run"] or (self.attack_cooldown == self.max_attack_cooldown): # check that the state shouldnt be anything else
            if self.movement_vector == [0,0] and not self.state == "idle":
                self.change_state("idle")
            elif self.movement_vector != [0,0] and not self.state == "run":
                self.change_state("run") # check for running state (called "run"
                
        self.collision_box["location"] = ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos)
        
        return False # Not dead
    
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
                
    def attack(self, player, entities, room, damage):
        from functions.algorithms.getMovementVector import get_movement_vector
        from classes.global_data import constants_structure
        constants = constants_structure()
        self.change_state("attack")
        self.attack_timer = 3
        
        range_vector = get_movement_vector(self.mele_reach, self.movement_vector)
        attack_loc = [(self.collision_box["location"][0] + (self.collision_box["size"][0]//2)) + range_vector[0],
                        (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)) + range_vector[1]]
        
        effectedEntities, effectedSquares, playerEffected = aoeScanner(attack_loc, entities, room, player, self.mele_reach, constants, True)
        
        # entities
        for entity in effectedEntities:
            if entity.team != self.team:
                entity.take_damage(damage)
                #entity_push = get_movement_vector(self.mele_push_strength, [attack_loc[0] - range_vector[0],
                #                                                            attack_loc[1] - range_vector[1]])
                #entity.move(entity_push, room, forced=True)
                
    def take_damage(self, damage):
        self.change_state("take_damage")
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def die(self):
        self.change_state("death")
    
    def draw(self, screen, FPS):
        
        #pygame.draw.rect(screen, (0, 0, 0), (self.x_pos, self.y_pos, 10,10))
        
        if (self.state == "idle" or
            self.state == "run" or
            self.state == "push" or
            self.state == "pull" or
            self.state == "attack"):
            animation = self.state + "_" + self.direction
            
        else:
            animation = self.state
            
        # select hand
        if self.holding_main_hand:
            if self.inventory[0] != None:
                item_texture = self.inventory[0].game_texture
        else:
            if self.inventory[1] != None:
                item_texture = self.inventory[1].game_texture
        if (self.holding_main_hand and self.inventory[0] != None) or ((not self.holding_main_hand) and self.inventory[1] != None):
            # find orientation and size
            if self.direction == "left" or self.direction == "up":
                item_texture = pygame.transform.flip(item_texture, True, False)
            item_texture = pygame.transform.scale(item_texture, (self.size[0]//3, self.size[1]//3))
            # blit to location
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            if self.direction == "left" or self.direction == "up":
                temp_surface.blit(item_texture, (15,50))
            else:
                temp_surface.blit(item_texture, ((self.size[0]//2)+10, 50))
            screen.blit(temp_surface, (self.x_pos, self.y_pos))
            
        # Player
        self.chosen_asset = self.assets[animation][self.animation_frame]
        
        temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(pygame.transform.scale(self.chosen_asset, self.size),(0,0))
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        self.animation_cooldown += 1
        if self.sprinting:
            self.animation_cooldown *= self.sprint_multiplier
        if self.animation_cooldown >= FPS // (1/self.animation_frame_time):
            self.animation_cooldown = 0
            self.animation_frame += 1
            
        
        if self.animation_frame == len(self.assets[animation]):
            self.animation_frame = 0
        
        
        # DRAW COLLISON BOX:
        #temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        #pygame.draw.rect(temp_surface, (255, 0, 0, 127), (0, 0, *self.collision_box["size"]))
        #screen.blit(temp_surface, self.collision_box["location"])
        
        return screen
    
    def draw_overlay_data(self, screen, room_location, room_size):
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        # Sprint energy
        sprint_energy_location = [room_location[0] - 60, constants.DEFAULT_SCREEN_SIZE[1]//2 + 130]
        sprint_energy_size = [20, 120]
        screen = draw_text("Sprint", screen, constants.SMALL_FONT, sprint_energy_location, (0,0,0), "centre", "below")
        # Black background
        pygame.draw.rect(screen, (0, 0, 0), (sprint_energy_location[0] - (sprint_energy_size[0]//2), sprint_energy_location[1] - sprint_energy_size[1] - 10, *sprint_energy_size))
        # Green fill
        bar_height = int(sprint_energy_size[1] * self.sprint_stamina / self.max_sprint_stamina)
        pygame.draw.rect(screen, (0, 255, 0), (sprint_energy_location[0] - (sprint_energy_size[0]//2), sprint_energy_location[1] - bar_height - 10, 
                                                sprint_energy_size[0], bar_height))
        
        # Boost energy
        boost_energy_location = [room_location[0] - 120, constants.DEFAULT_SCREEN_SIZE[1]//2 + 130]
        boost_energy_size = [20, 120]
        screen = draw_text("Boost", screen, constants.SMALL_FONT, boost_energy_location, (0,0,0), "centre", "below")
        # Black background
        pygame.draw.rect(screen, (0, 0, 0), (boost_energy_location[0] - (boost_energy_size[0]//2), boost_energy_location[1] - boost_energy_size[1] - 10, *boost_energy_size))
        # Green fill
        bar_height = int(boost_energy_size[1] * self.boost_cooldown / self.max_boost_time)
        pygame.draw.rect(screen, (0, 255, 0), (boost_energy_location[0] - (boost_energy_size[0]//2), boost_energy_location[1] - bar_height - 10, 
                                                boost_energy_size[0], bar_height))
        
        
        # Health
        health_bar_location = [constants.DEFAULT_SCREEN_SIZE[0]//2, room_location[1] - 20]
        health_bar_size = [150, 20]
        screen = draw_text("Health", screen, constants.SMALL_FONT, health_bar_location, (0,0,0), "centre", "below")
        # Black background
        pygame.draw.rect(screen, (0, 0, 0), (health_bar_location[0] - (health_bar_size[0]//2), health_bar_location[1] - health_bar_size[1] - 10, *health_bar_size))
        # Green fill
        bar_width = int(health_bar_size[0] * self.health / self.max_health)
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_location[0] - (health_bar_size[0]//2), health_bar_location[1] - health_bar_size[1] - 10, 
                                                bar_width, health_bar_size[1]))
        
        
        
        
        # INVENTORY
        inv_location = (room_location[0] + room_size[0] + 20, int((constants.DEFAULT_SCREEN_SIZE[1]//2) - (2.5*constants.INV_ITEM_SIZE[1])))
        temp_surface = pygame.Surface(constants.DEFAULT_SCREEN_SIZE, pygame.SRCALPHA) 
        temp_surface.blit(self.inv_texture, inv_location)
        screen.blit(temp_surface, (0,0))
        if self.holding_main_hand:
            temp_surface.blit(self.selected_inv_texture, (inv_location[0] + 3, inv_location[1] + (constants.INV_ITEM_SIZE[1] * 4)))
        else:
            temp_surface.blit(self.selected_inv_texture, (inv_location[0] - 3 + (constants.INV_ITEM_SIZE[0] * 2), inv_location[1] + (constants.INV_ITEM_SIZE[1] * 4)))
        screen.blit(temp_surface, (0,0))
        
        if self.inventory[0] != None:
            # print("has mainhand")
            self.inventory[0].draw_inv(screen, (inv_location[0], inv_location[1] + (4*constants.INV_ITEM_SIZE[1])))
            #temp_surface.blit(pygame.transform.scale(self.inventory[0].inv_texture, constants.INV_ITEM_SIZE), (inv_location[0], inv_location[1] + (4*constants.INV_ITEM_SIZE[1])))
        
        #screen.blit(self.inv_square_texture, (inv_location[0] + (2*constants.INV_ITEM_SIZE[0]), inv_location[1] + (4*constants.INV_ITEM_SIZE[1])))
        if self.inventory[1] != None:
            self.inventory[1].draw_inv(screen, (inv_location[0] + (2*constants.INV_ITEM_SIZE[0]), inv_location[1] + (4*constants.INV_ITEM_SIZE[1])))
        
        for row in range(4):
            for item in range(3):
                item_i = 2 + (row * 3) + item
                #screen.blit(self.inv_square_texture, (inv_location[0] + (item*constants.INV_ITEM_SIZE[0]), inv_location[1] + (row*constants.INV_ITEM_SIZE[1])))
                if self.inventory[item_i] != None:
                    self.inventory[item_i].draw_inv(screen, (inv_location[0] + (item*constants.INV_ITEM_SIZE[0]), inv_location[1] + (row*constants.INV_ITEM_SIZE[1])))
        
        #screen.blit(temp_surface, (0,0))
        
        return screen
    
    def initiate_assets(self, constants):
        self.assets = {}
        #with open(constants.FILE_PATH + "project_lib/assets/player/main.png", 'r') as asset_file:
        
        
        master_texture = pygame.image.load(constants.FILE_PATH + "project_lib/assets/player/main.png").convert() # Use text input button design
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

        # DRAW BOOST ANIMATION