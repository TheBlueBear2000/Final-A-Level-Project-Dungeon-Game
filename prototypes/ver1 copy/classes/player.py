import pygame


class Player:
    def __init__(self, x, y):
        # Constants
        from classes.global_data import constants_structure
        constants = constants_structure()

        self.initiate_assets(constants)
        
        self.state = "idle"
        self.direction = "down"
        
        self.x_pos = x
        self.y_pos = y
        self.movement_vector = [0,0]
        self.speed = 6
        self.size = (150,150)
        self.sprinting = False
        self.sprint_multiplier = 2
        self.sprint_stamina = 45
        self.boost_cooldown = 75
        self.animation_frame_time = 0.1
        self.animation_cooldown = 0
        
        self.inventory = []
        self.holding_main_hand = True
        
        # possible states: idle, run, sprint, boost, push, pull, attack, take_damage, death, fall
        self.change_state("idle")
        
        
    def move(self, key_bindings, events):
            
        started_movements = []
        ended_movements = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) is not None: # key values are equal to the decimal ascii value of that key
                    started_movements.append(key_bindings[str(event.key)])
            if event.type == pygame.KEYUP:
                if key_bindings.get(str(event.key)) is not None: # key values are equal to the decimal ascii value of that key
                    ended_movements.append(key_bindings[str(event.key)])
        
        
        # Start togglable movements
        for movement in started_movements:
            multiplier = 1
            if self.sprinting:
                multiplier = self.sprint_multiplier
            if movement == "up":
                self.movement_vector[1] = -1 * self.speed * multiplier
                self.check_direction()
                    
            elif movement == "down":
                self.movement_vector[1] = self.speed * multiplier
                self.check_direction()
                    
            elif movement == "left":
                self.movement_vector[0] = -1 * self.speed * multiplier
                self.check_direction()
                
            elif movement == "right":
                self.movement_vector[0] = self.speed * multiplier
                self.check_direction()
                
            elif movement == "sprint":
                if self.sprint_stamina > 0:
                    self.sprinting = True
                
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
                run_pause_screen()
            elif movement == "inventory":
                from functions.loops.inventory import run as open_inventory
                open_inventory()
            # IMPLEMENT BOOST FUNCTIONALITY                                                             #####
                self.boost_cooldown = 0
                
        
        # end movements
        for movement in ended_movements:
            if movement == "up" or movement == "down":
                self.movement_vector[1] = 0
                self.check_direction()
            elif movement == "left" or movement == "right":
                self.movement_vector[0] = 0
                self.check_direction()
            elif movement == "sprint":
                self.sprinting = False
        
        # adjust stamina
        if self.sprinting and self.sprint_stamina > 0:
            self.sprint_stamina -= 1
        elif self.sprint_stamina < 45:
            self.sprint_stamina += 1
        
        if self.sprint_stamina == 0:
            self.sprinting = False
        print(self.sprint_stamina)
        # adjust boost cooldown
        if self.boost_cooldown < 75:
            self.boost_cooldown += 1
                    
        # CALCULATE MOVEMENT VECTOR
        speed = self.speed # handle sprinting (replace later to account for pushing or non-sprinting states)
        if self.sprinting:
            speed *= self.sprint_multiplier
        from functions.algorithms.getMovementVector import get_movement_vector
        self.movement_vector = get_movement_vector(speed, self.movement_vector)
        
        # IMPLEMENT COLLISION CHECK LATER                                                                             ####
        
        # DO ACTUAL MOVEMENT
        self.x_pos += self.movement_vector[0]
        self.y_pos += self.movement_vector[1]
        
        
        # CURRENTLY WORKING ON:
        # calculate movement state change
        if self.state in ["idle", "run"]: # check that the state shouldnt be anything else
            if self.movement_vector == [0,0] and not self.state == "idle":
                self.change_state("idle")
            elif self.movement_vector != [0,0] and not self.state == "run":
                self.change_state("run") # check for running state (called "run")
    
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
    
    def draw(self, screen, FPS):
        
        pygame.draw.rect(screen, (0, 0, 0), (self.x_pos, self.y_pos, 10,10))
        
        if (self.state == "idle" or
            self.state == "run" or
            self.state == "push" or
            self.state == "pull" or
            self.state == "attack"):
            animation = self.state + "_" + self.direction
            
        else:
            animation = self.state
            
        print(animation)
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