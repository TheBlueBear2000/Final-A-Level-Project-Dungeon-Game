import pygame
from functions.algorithms.aoeScanner import aoeScanner
from functions.algorithms.item_lookup import lookup
from classes.items.living_item import LivingItem
from math import sqrt
from random import randint


class Player:
    def __init__(self, level, account_id, savegame_id):
        import json
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Extract player data
        player_data = json.load(open(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels/rooms_{level}/player.json", "r"))

        # Set all attributes (most data extracted from player data)
        self.account_id = account_id
        self.savegame_id = savegame_id
        
        self.initiate_assets(constants)
        
        self.state = "idle"
        self.direction = player_data["direction"]
        
        self.lives = player_data["lives"]
        
        self.max_health = player_data["max_health"]
        self.health = player_data["health"]
        self.x_pos = player_data["x"] if player_data["x"] is not None else constants.GAME_WINDOW_SIZE[0]//2 - 75   #x if x is not None else player_data["x"]
        self.y_pos = player_data["y"] if player_data["y"] is not None else constants.GAME_WINDOW_SIZE[1]//2 - 75   #y if y is not None else player_data["y"]
        self.current_room = player_data["current_room"]
        self.movement_vector = [0,0]
        self.speed = player_data["speed"]
        self.push_pull_speed = player_data["push_pull_speed"]
        self.size = (150,150)
        self.sprinting = False
        self.push_speed_multiplier = 0.3
        self.pushing = False
        self.sprint_multiplier = 2
        self.max_sprint_stamina = player_data["max_sprint_stamina"]
        self.sprint_stamina = player_data["sprint_stamina"]
        self.max_boost_time = player_data["max_boost_time"]
        self.boost_cooldown = player_data["boost_cooldown"]
        self.boost_frame = 0
        self.boost_speed = player_data["boost_speed"]
        self.animation_frame_time = 0.1
        self.animation_cooldown = 0
        
        self.mele_reach = player_data["mele_reach"]
        self.mele_push_strength = player_data["mele_push_strength"]
        self.attack_damage = player_data["attack_damage"]
        self.attack_timer = 0
        self.max_attack_cooldown = player_data["max_attack_cooldown"]
        self.attack_cooldown = self.max_attack_cooldown
        
        self.team = "player"
        
        self.held_keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "sprint": False
        }
        
        self.collision_box = {"size": (48, 25),
                            "location": ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 40 + self.y_pos)}
        
        # Inventory
        inventory_data = player_data["inventory"]
        
        from functions.algorithms.item_lookup import lookup as i_lookup
        self.inventory = []
        for item in inventory_data:
            if item is not None:
                self.inventory.append(i_lookup(item["item"])(item["payload"])) # Translate item IDs into item objects to populate inventory
            else:
                self.inventory.append(None)
        
        
        # General textures
        self.inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory.png").convert(), (constants.INV_ITEM_SIZE[0] * 3, constants.INV_ITEM_SIZE[1] * 5))
        self.selected_inv_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/inventory_highlighted.png").convert(), constants.INV_ITEM_SIZE)
        self.holding_main_hand = player_data["holding_main_hand"]
        
        self.lives_texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + f"project_lib/assets/menu/icons/player_head.png").convert(), constants.LIVES_SIZE)
        
        self.side_bar_asset = pygame.image.load(constants.FILE_PATH + "project_lib/assets/menu/side_bar.png")
        
        self.get_square = lambda room : [int((self.collision_box["location"][0] - room.location[0])//constants.SQUARE_SIZE[0]),
                                        int((self.collision_box["location"][1] - room.location[1])//constants.SQUARE_SIZE[1])]
        
        
        # possible states: idle, run, sprint, boost, push, pull, attack, take_damage, death, fall
        self.change_state("idle")
        
        # Statistics
        self.kills = player_data["kills"]
        
        
    def move(self, key_bindings, events, room_data, entities, living_items, crates, levers, doors, room, screen):
        # Prioritise non-processing animations (death)
        if self.state == "death":
            if self.animation_frame == len(self.assets["death"])-1:
                return True, living_items, True # Running death animation
            else:
                return False, living_items, True # Finally dead

        
        throw_away_items = [] # Items that will be thrown out of the players inventory later and turned into living items
        
        # Increment attack cooldown
        if self.attack_cooldown < self.max_attack_cooldown:
            self.attack_cooldown += 1 * self.get_attack_speed_multiplier()
        
        # Keep track of actions in this frame
        started_movements = []
        ended_movements = []
        for event in events:
            # Tracks what keys have been pressed or unpressed
            if event.type == pygame.KEYDOWN:
                if key_bindings.get(str(event.key)) is not None: # key values are equal to the decimal ascii value of that key
                    started_movements.append(key_bindings[str(event.key)])
            if event.type == pygame.KEYUP:
                if key_bindings.get(str(event.key)) is not None: # key values are equal to the decimal ascii value of that key
                    ended_movements.append(key_bindings[str(event.key)])
            # Tracks what mouse buttons have been pressed or unpressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if key_bindings.get("L_CLICK") is not None:
                    started_movements.append(key_bindings["L_CLICK"])
            if event.type == pygame.MOUSEBUTTONUP:
                if key_bindings.get("L_CLICK") is not None:
                    started_movements.append(key_bindings["L_CLICK"])

        
        
        
        
        # Start togglable movements
        for movement in started_movements:
            # Directional movements
            # Held Keys are keys where the state needs to referenced every frame, rather than only being triggered when they are hit
            # For example, when holding the up key, you want the player to continue to do the action until you release the key, but
            # with something like attacking, you only want them to attack when you click, and then you should have to click again
            # in order to attack again.
            if movement == "up":
                self.held_keys["up"] = True
            elif movement == "down":
                self.held_keys["down"] = True
            elif movement == "left":
                self.held_keys["left"] = True
            elif movement == "right":
                self.held_keys["right"] = True
                
            elif movement == "sprint":
                self.held_keys["sprint"] = True
                if self.sprint_stamina > 0:
                    self.sprinting = True
                    
            elif movement == "attack":
                if self.attack_cooldown >= self.max_attack_cooldown: # Check if attack is possible
                    self.attack_cooldown = 0
                    attack_damage = self.attack_damage # Default
                    # calculate new damage from weapon
                    if self.holding_main_hand and (self.inventory[0] != None): # Mainhand
                        attack_damage = self.attack_damage * self.inventory[0].damage_multiplier
                    elif (not self.holding_main_hand) and (self.inventory[1] != None): # Offhand
                        attack_damage = self.attack_damage * self.inventory[1].damage_multiplier
                        
                    # Run attack
                    drops = self.attack(self, entities, room, attack_damage)
                    
                    # Handle drops from attack
                    for item in drops:
                        if item["name"] != None:
                            living_items.append(LivingItem(item["x"], item["y"], lookup(item["name"]["item"])(item["name"]["payload"]), [randint(-10,10), randint(-10,10)]))
                            
                
            # Hand selection (boolean determines where in inventory array will be selected, since index 0 and 1 are the main and off hand respectively)
            elif movement == "switch_hand": # Toggle
                self.holding_main_hand = not self.holding_main_hand
            elif movement == "main_hand": # Main
                self.holding_main_hand = True
            elif movement == "off_hand": # Off
                self.holding_main_hand = False
                
            # Run screen buttons
            elif movement == "pause": # Pause screen
                from functions.loops.pause_screen import run as run_pause_screen
                continue_game = run_pause_screen(screen, key_bindings)
                # Pause screen might tell player to quit game, which needs to be brought back to game loop shell by returning values
                if not continue_game:
                    return False, living_items, False # Last false means that game must be quit
                
                self.reassess_keys(key_bindings) # Manually reassess what keys are pressed
                
            elif movement == "inventory": # Inventory screen
                from functions.loops.inventory import run as open_inventory
                self.inventory, throw_away_items = open_inventory(self.inventory, screen, key_bindings) # Get items removed from inventory after inventory closed
                
                self.reassess_keys(key_bindings)# Manually reassess what keys are pressed
                
            # Boost functionality
            elif movement == "boost":
                # Boost will only run if player is moving to prevent accidental use
                if self.boost_cooldown == self.max_boost_time  and  (self.held_keys["up"] or self.held_keys["down"] or self.held_keys["left"] or self.held_keys["right"]):
                    self.boost_cooldown = 0
                    self.boost_frame = 3
                    
            elif movement == "interact":
                # check for item pickup
                if len(living_items) > 0:
                    item = None
                    distance = 9999999999999
                    for l_item in living_items:
                        n_distance = sqrt((((l_item.x_pos + (l_item.size[0]//2)) - (self.collision_box["location"][0] + (self.collision_box["size"][0]//2)))  **2)  +
                                        (((l_item.y_pos + (l_item.size[1]//2)) - (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)))  **2))
                        if n_distance < distance:
                            item = l_item
                            distance = n_distance
                        
                    if distance < 60:
                        living_items = self.pick_up(item, living_items)
                        break # break from interaction
                    
                # check for doors to be opened
                if len(doors) > 0:
                    door = None
                    distance = 9999999999999
                    for n_door in doors:
                        if n_door.manual or n_door.type == "keyhole":
                            n_distance = sqrt((((n_door.collision_box["location"][0] + (n_door.collision_box["size"][0]//2)) - (self.collision_box["location"][0] + (self.collision_box["size"][0]//2)))  **2)  +
                                            (((n_door.collision_box["location"][1] + (n_door.collision_box["size"][1]//2)) - (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)))  **2))
                            if n_distance < distance:
                                door = n_door
                                distance = n_distance
                                
                        
                    if distance < 90:
                        if door.type == "keyhole": # Keyhole doors require current hand to contain correct key
                            if self.inventory[1-int(self.holding_main_hand)] != None:
                                if self.inventory[1-int(self.holding_main_hand)].type == "key":
                                    if self.inventory[1-int(self.holding_main_hand)].colour == door.colour:
                                        door.toggle_state()
                                        if door.side is not None:
                                            room.complete_objective(door.side)
                        else:
                            door.toggle_state() # Normal door
                        break # break from interaction
                        
                # check for levers to be flicked
                if len(levers) > 0:
                    lever = None
                    distance = 9999999999999
                    for n_lever in levers:
                        n_distance = sqrt((((n_lever.collision_box["location"][0] + (n_lever.collision_box["size"][0]//2)) - (self.collision_box["location"][0] + (self.collision_box["size"][0]//2)))  **2)  +
                                        (((n_lever.collision_box["location"][1] + (n_lever.collision_box["size"][1]//2)) - (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)))  **2))
                        if n_distance < distance:
                            lever = n_lever
                            distance = n_distance
                        
                    if distance < 60:
                        lever.flicked = not lever.flicked # toggle
                        break # break from interaction
        
        # end movements (only held keys)
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
                self.held_keys["sprint"] = False
                
        # Calculate speed based on sprinting
        multiplier = self.get_speed_multiplier() # Multiplier based on current equipment
        if self.sprinting:
            multiplier = self.sprint_multiplier
            
        
        # create vector from held keys
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
        if self.sprinting and self.sprint_stamina > 0 and (not self.pushing):
            self.sprint_stamina -= 1
        elif self.sprint_stamina < 45 and (not self.pushing):
            self.sprint_stamina += 1 * self.get_stamina_recharge_multiplier()
        
        if self.sprint_stamina == 0:
            self.sprinting = False
        
        # adjust boost cooldown
        if self.boost_cooldown < self.max_boost_time:
            self.boost_cooldown += 1
                    
                    
        moves = 1
        boosting = False
        if self.boost_frame > 0:
            boosting = True
            self.boost_frame -= 1 * self.get_stamina_recharge_multiplier()
            moves = self.boost_speed
            
            
        # CALCULATE MOVEMENT VECTOR
        speed = self.speed * self.get_speed_multiplier()
        if self.sprinting and not boosting:
            speed *= self.sprint_multiplier
        # Uses direction vector and scales it to work for movement speed, so that movement in any direction has a uniform speed
        from functions.algorithms.getMovementVector import get_movement_vector
        self.movement_vector = get_movement_vector(speed, self.movement_vector)
        
        
        
        from functions.algorithms.collision_detection import is_colliding, collision
        from classes.global_data import constants_structure
        constants = constants_structure()
        self.pushing = False
        for i in range(moves): # Check every step so that player can walk right up to wall
            self.collision_box["location"] = ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos)
            # Calculate X direction
            projected_collision_box = self.collision_box
            for x_distance in range(abs(int(self.movement_vector[0]))):
                # Cast collision box
                self.collision_box["location"] = ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos)
                projected_collision_box = {
                    "size": projected_collision_box["size"],
                    "location": (projected_collision_box["location"][0] + (self.movement_vector[0]/abs(self.movement_vector[0])), projected_collision_box["location"][1])
                }
                # Check for square collisions
                if not is_colliding(projected_collision_box, room_data["layout"], room_data["location"], constants.SQUARE_SIZE): # wall collision
                    is_crate_collision = False
                    pushed_x = False
                    collided_door = False
                    # Check for door collisions
                    for door in doors:
                        if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                            collided_door = True
                            break
                    if not collided_door:
                        # Check for crate collisions
                        for crate in crates:
                            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*crate.collision_box["location"], *crate.collision_box["size"]]):
                                is_crate_collision = True
                                if self.held_keys["sprint"]:
                                    self.pushing = True
                                    if crate.move("left" if self.movement_vector[0] < 0 else "right", self.push_speed_multiplier, room, crates, doors, entities, []):
                                        if not pushed_x:
                                            pushed_x = True
                                            self.x_pos += (self.movement_vector[0]/abs(self.movement_vector[0])) * self.push_speed_multiplier
                    # Carry out move if possible
                    if not (is_crate_collision or collided_door):
                        self.x_pos += (self.movement_vector[0]/abs(self.movement_vector[0]))
                
            # Calculate Y direction
            projected_collision_box = self.collision_box
            for y_distance in range(abs(int(self.movement_vector[1]))):
                # Cast collision box
                self.collision_box["location"] = ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos)
                projected_collision_box = {
                    "size": projected_collision_box["size"],
                    "location": (projected_collision_box["location"][0], projected_collision_box["location"][1] + (self.movement_vector[1]/abs(self.movement_vector[1])))
                }
                # Check for square collisions
                if not is_colliding(projected_collision_box, room_data["layout"], room_data["location"], constants.SQUARE_SIZE):
                    is_crate_collision = False
                    pushed_y = False
                    collided_door = False
                    # Check for door collisions
                    for door in doors:
                        if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*door.collision_box["location"], *door.collision_box["size"]]):
                            collided_door = True
                            break
                    if not collided_door:
                        # Check for crate collisions
                        for crate in crates:
                            if collision([*projected_collision_box["location"], *projected_collision_box["size"]], [*crate.collision_box["location"], *crate.collision_box["size"]]):
                                is_crate_collision = True
                                if self.held_keys["sprint"]:
                                    self.pushing = True
                                    if crate.move("up" if self.movement_vector[1] < 0 else "down", self.push_speed_multiplier, room, crates, doors, entities, []):
                                        if not pushed_y:
                                            pushed_y = True
                                            self.y_pos += (self.movement_vector[1]/abs(self.movement_vector[1])) * self.push_speed_multiplier
                    # Carry out move if possible
                    if not (is_crate_collision or collided_door):
                        self.y_pos += (self.movement_vector[1]/abs(self.movement_vector[1]))
        
        
        # Calculate state changes
        if (self.state in ["idle", "run"] or (self.attack_cooldown == self.max_attack_cooldown)) and not self.pushing: # check that the state shouldn't be anything else
            if self.movement_vector == [0,0] and not self.state == "idle":
                self.change_state("idle")
            elif self.movement_vector != [0,0] and not self.state == "run":
                self.change_state("run")
                
        elif self.pushing and self.state != "push":
            self.change_state("push")
            
        # Update collision box
        self.collision_box["location"] = ((self.size[0]-48)//2 + self.x_pos, (self.size[1]-20)//2 + 23 + self.y_pos)
        
        # Turn thrown away items into living items and add them to the living items list
        for item in throw_away_items:
            throwing_velocity = 10
            if self.direction == "right":
                throwing_direction = [throwing_velocity,0]
            elif self.direction == "left":
                throwing_direction = [-1 * throwing_velocity,0]
            elif self.direction == "up":
                throwing_direction = [0,-1 * throwing_velocity]
            elif self.direction == "down":
                throwing_direction = [0,throwing_velocity]
            living_items.append(LivingItem(self.collision_box["location"][0] + (self.collision_box["size"][0]//2) + randint(0,20)-10,
                                            self.collision_box["location"][1] + randint(0,20)-10,
                                            item,
                                            throwing_direction))
        
        return False, living_items, True # Return all updated data back to main function
    
    
    def get_damage_multiplier(self): # not including hand (that is dealt with seperately)
        multiplier = 1
        for i in range(3): # Charms
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].damage_multiplier
        return multiplier
    
    def get_speed_multiplier(self):
        multiplier = 1
        for i in range(6): # Charms and armour
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].speed_multiplier
        return multiplier
    
    def get_mele_armour_multiplier(self):
        multiplier = 1
        for i in range(6): # Charms and armour
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].mele_armour_multiplier
        return multiplier
    
    # NOT IMPLEMENTED DUE TO NO RANGED WEAPONS
    def get_ranged_armour_multiplier(self):
        multiplier = 1
        for i in range(6): # Charms and armour
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].ranged_armour_multiplier
        return multiplier
    
    def get_attack_speed_multiplier(self): # not including hand (that is dealt with seperately)
        multiplier = 1
        for i in range(3): # Charms
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].attack_speed_multiplier
        return multiplier
        
    # NOT IMPLEMENTED DUE TO NO RANGED WEAPONS
    def get_ranged_reload_multiplier(self):
        multiplier = 1
        for i in range(3): # Charms
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].ranged_reload_multiplier
        return multiplier
    
    # NOT IMPLEMENTED DUE TO NO CHARMS
    def get_max_health_multiplier(self):
        multiplier = 1
        for i in range(3): # Charms
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].max_health_multiplier
        return multiplier
    
    # NOT IMPLEMENTED
    def get_regen_speed(self):
        speed = 0
        for i in range(3): # Charms
            if self.inventory[8+i] != None:
                multiplier += self.inventory[8+i].regen_speed
        return speed
    
    def get_stamina_recharge_multiplier(self):
        multiplier = 1
        for i in range(3): # Charms
            if self.inventory[8+i] != None:
                multiplier *= self.inventory[8+i].stamina_recharge_multiplier
        return multiplier
        
        
    
    def teleport(self, x, y): # Manually sets coordinates if needed
        self.x_pos = x
        self.y_pos = y
        
    def reassess_keys(self, key_bindings): # Manually reassess the state of all held keys
        keys = pygame.key.get_pressed()
        for key in key_bindings:
            if key_bindings[key] in self.held_keys:
                self.held_keys[key_bindings[key]] = keys[int(key)]
            
    def change_state(self, new_state): # Update state and reset animation frame
        self.state = new_state
        self.animation_frame = 0
    
    def check_direction(self):
        # Calculate direction based off of movement vector
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
    
    def pick_up(self, living_item, living_items):
        if None in self.inventory: # If inventory has space
            for s, slot in enumerate(self.inventory):
                if slot == None:
                    # Add item to empty slot
                    self.inventory[s] = living_item.item 
                    # Remove item from ground
                    for i, item in enumerate(living_items):
                        if living_item == item:
                            living_items.pop(i)
                            break
                    break
        return living_items
                
    def attack(self, player, entities, room, damage):
        from functions.algorithms.getMovementVector import get_movement_vector
        from classes.global_data import constants_structure
        constants = constants_structure()
        # Start attack animation
        self.change_state("attack")
        self.attack_timer = 3
        
        # Calculate how much damage should be done to effected objects
        damage *= self.get_damage_multiplier()
        
        multiplier = 1
        if self.inventory[(0 if self.holding_main_hand else 1)] != None:
            multiplier = self.inventory[(0 if self.holding_main_hand else 1)].mele_range_multiplier
        
        # Calculate attack range
        reach = self.mele_reach * multiplier
        range_vector = get_movement_vector(reach, self.movement_vector)
        attack_loc = [(self.collision_box["location"][0] + (self.collision_box["size"][0]//2)) + range_vector[0],
                        (self.collision_box["location"][1] + (self.collision_box["size"][1]//2)) + range_vector[1]]
        
        # Get lists of effected entities and squares
        effectedEntities, effectedSquares, playerEffected = aoeScanner(attack_loc, entities, room, player, reach, constants, True)
        
        drops = []
        
        # Entities
        for entity in effectedEntities:
            if entity.team != self.team:
                killed, entity_drops = entity.take_damage(damage) # returns true if entity is killed
                if killed:
                    self.kills += 1
                    room.kills += 1
                for drop in entity_drops:
                    drops.append({"name": drop, 
                                    "x": entity.collision_box["location"][0],
                                    "y": entity.collision_box["location"][1]})
        
        # Squares
        for square in effectedSquares:
            square_obj = room.layout[square[1]][square[0]]
            if square_obj.breakable:
                square_drops = square_obj.take_damage(damage, room)
                for drop in square_drops:
                    drops.append({"name": drop, 
                                    "x": square[0]*constants.SQUARE_SIZE[0] + room.location[0],
                                    "y": square[1]*constants.SQUARE_SIZE[1] + room.location[1]})
        
        return drops
                
    def take_damage(self, damage, damage_type="mele"):
        self.change_state("take_damage")
        
        # Reduce incoming damage based on armour stats
        if damage_type == "mele":
            damage *= self.get_mele_armour_multiplier()
        elif damage_type == "ranged": # NOT YET FULLY IMPLEMENTED
            damage *= self.get_ranged_armour_multiplier()
        
        # Do damage and check for death
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def die(self):
        # Start death sequence
        self.change_state("death")
        
        
    def save(self, level, room_id):
        import json
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # Turn inventory objects back into strings
        inventory_data = []
        for item in self.inventory:
            if item is not None:
                inventory_data.append(item.save())
            else:
                inventory_data.append(None)
        
        # Construct data
        data = {
        "lives": self.lives,
        "max_health": self.max_health,
        "health": self.health,
        "x": self.x_pos,
        "y": self.y_pos,
        "current_room": room_id,
        "direction": self.direction,
        "speed": self.speed,
        "push_pull_speed": self.push_pull_speed,
        "max_sprint_stamina": self.max_sprint_stamina,
        "sprint_stamina": self.sprint_stamina,
        "max_boost_time": self.max_boost_time,
        "boost_cooldown": self.boost_cooldown,
        "boost_speed": self.boost_speed,

        "mele_reach": self.mele_reach,
        "mele_push_strength": self.mele_push_strength,
        "attack_damage": self.attack_damage,
        "max_attack_cooldown": self.max_attack_cooldown,

        "inventory": inventory_data,

        "holding_main_hand": self.holding_main_hand,

        "kills": self.kills
        }
        
        # Write data to file
        with open(constants.FILE_PATH + f"data/account_games/{self.account_id}_games/{self.savegame_id}_levels/rooms_{level}/player.json", 'w') as file:
            json_string = json.dumps(data)
            file.write(json_string)
    
    def get_rendering_row(self):
        return self.collision_box["location"][1]
    
    def draw(self, screen):
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        FPS = constants.MENU_FPS * 2
        
        # Get animation name for direction states
        if (self.state == "idle" or
            self.state == "run" or
            self.state == "push" or
            self.state == "pull" or
            self.state == "attack"):
            animation = self.state + "_" + self.direction
        # Get animation name for non-directional states
        else:
            animation = self.state
            
            
        # HAND ITEM
        
        # Select hand item texture to draw
        self.hand_texture = pygame.Surface((1,1), pygame.SRCALPHA)
        if self.holding_main_hand:
            if self.inventory[0] != None:
                item_texture = self.inventory[0].game_texture
        else:
            if self.inventory[1] != None:
                item_texture = self.inventory[1].game_texture
        
        if (self.holding_main_hand and self.inventory[0] != None) or ((not self.holding_main_hand) and self.inventory[1] != None):
            # Rotate for attack type to draw animation
            if self.state == "attack":
                item_texture = pygame.transform.rotate(item_texture, self.animation_frame * -60)
            # Find orientation and size
            if self.direction == "left" or self.direction == "up":
                item_texture = pygame.transform.flip(item_texture, True, False)
            item_texture = pygame.transform.scale(item_texture, (self.size[0]//3, self.size[1]//3))
            # Draw to location
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            if self.direction == "left" or self.direction == "up":
                temp_surface.blit(item_texture, (15,50))
            else:
                temp_surface.blit(item_texture, ((self.size[0]//2)+10, 50))
            self.hand_texture = temp_surface
            screen.blit(temp_surface, (self.x_pos, self.y_pos))
            
            
        # Player
        
        # Calculate animation frame
        self.animation_cooldown += 1
        if self.sprinting:
            self.animation_cooldown *= self.sprint_multiplier
        if self.animation_cooldown >= FPS // (1/self.animation_frame_time):
            self.animation_cooldown = 0
            self.animation_frame += 1
            
        
        if self.animation_frame >= len(self.assets[animation]):
            self.animation_frame = 0
        
        self.chosen_asset = self.assets[animation][self.animation_frame]
        
        # Draw animation frame
        # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) 
        temp_surface.blit(pygame.transform.scale(self.chosen_asset, self.size),(0,0))
        screen.blit(temp_surface, (self.x_pos, self.y_pos))
        
        # Code to draw collision box for development:
        # temp_surface = pygame.Surface(self.size, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        # pygame.draw.rect(temp_surface, (255, 0, 0, 127), (0, 0, *self.collision_box["size"]))
        # screen.blit(temp_surface, self.collision_box["location"])
        
        return screen
    
    def draw_overlay_data(self, screen, room_location, room_size):
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        # Draw side-bar
        temp_surface = pygame.Surface(constants.GUI_WINDOW_SIZE, pygame.SRCALPHA) 
        side_bar = self.side_bar_asset
        if not constants.LANDSCAPE:
            side_bar = pygame.transform.rotate(side_bar, 90)
        temp_surface.blit(pygame.transform.scale(side_bar, constants.GUI_WINDOW_SIZE), (0,0))
        screen.blit(temp_surface, (0,0))
        
        
        # Draw sprint energy
        sprint_energy_location = [(constants.GUI_WINDOW_SIZE[0] - self.inv_texture.get_width())//2 + (self.inv_texture.get_width() // 4 * 3), 20 + self.inv_texture.get_height() + 100]
        sprint_energy_size = [self.inv_texture.get_width() // 2 - 40, 20]
        screen = draw_text("Sprint", screen, constants.SMALL_FONT, sprint_energy_location, (255,255,255), "centre", "below")
        # Black background
        pygame.draw.rect(screen, (0, 0, 0), (sprint_energy_location[0] - (sprint_energy_size[0]//2), sprint_energy_location[1] - sprint_energy_size[1] - 10, *sprint_energy_size))
        # Green fill
        bar_width = int(sprint_energy_size[0] * self.sprint_stamina / self.max_sprint_stamina)
        pygame.draw.rect(screen, (0, 255, 0), (sprint_energy_location[0] - (sprint_energy_size[0]//2), sprint_energy_location[1] - 30, 
                                                bar_width, sprint_energy_size[1]))
        
        # Draw boost energy
        boost_energy_location = [(constants.GUI_WINDOW_SIZE[0] - self.inv_texture.get_width())//2 + (self.inv_texture.get_width() // 4), 20 + self.inv_texture.get_height() + 100]
        boost_energy_size = [self.inv_texture.get_width() // 2 - 40, 20]
        screen = draw_text("Boost", screen, constants.SMALL_FONT, boost_energy_location, (255,255,255), "centre", "below")
        # Black background
        pygame.draw.rect(screen, (0, 0, 0), (boost_energy_location[0] - (boost_energy_size[0]//2), boost_energy_location[1] - boost_energy_size[1] - 10, *boost_energy_size))
        # Green fill
        bar_width = int(boost_energy_size[0] * self.boost_cooldown / self.max_boost_time)
        pygame.draw.rect(screen, (0, 255, 0), (boost_energy_location[0] - (boost_energy_size[0]//2), boost_energy_location[1] - 30, 
                                                bar_width, boost_energy_size[1]))
        
        
        # Draw health
        health_bar_location = [(constants.GUI_WINDOW_SIZE[0] - self.inv_texture.get_width())//2 + (self.inv_texture.get_width() // 2), 20 + self.inv_texture.get_height() + 40]
        health_bar_size = [self.inv_texture.get_width(), 20]
        screen = draw_text("Health", screen, constants.SMALL_FONT, health_bar_location, (255,255,255), "centre", "below")
        # Black background
        pygame.draw.rect(screen, (0, 0, 0), (health_bar_location[0] - (health_bar_size[0]//2), health_bar_location[1] - health_bar_size[1] - 10, *health_bar_size))
        # Green fill
        bar_width = int(health_bar_size[0] * self.health / self.max_health)
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_location[0] - (health_bar_size[0]//2), health_bar_location[1] - health_bar_size[1] - 10, 
                                                bar_width, health_bar_size[1]))
        
        
        # Draw inventory
        inv_location = ((constants.GUI_WINDOW_SIZE[0] - self.inv_texture.get_width())//2, 20)
        temp_surface = pygame.Surface(constants.GUI_WINDOW_SIZE, pygame.SRCALPHA) 
        temp_surface.blit(self.inv_texture, inv_location)
        
        # Draw selected square 
        screen.blit(temp_surface, (0,0))
        if self.holding_main_hand:
            temp_surface.blit(self.selected_inv_texture, (inv_location[0] + 3, inv_location[1] + (constants.INV_ITEM_SIZE[1] * 4)))
        else:
            temp_surface.blit(self.selected_inv_texture, (inv_location[0] - 3 + (constants.INV_ITEM_SIZE[0] * 2), inv_location[1] + (constants.INV_ITEM_SIZE[1] * 4)))
        screen.blit(temp_surface, (0,0))
        
        # Manually draw lower two items since order is odd
        if self.inventory[0] != None:
            self.inventory[0].draw_inv(screen, (inv_location[0], inv_location[1] + (4*constants.INV_ITEM_SIZE[1])))
        if self.inventory[1] != None:
            self.inventory[1].draw_inv(screen, (inv_location[0] + (2*constants.INV_ITEM_SIZE[0]), inv_location[1] + (4*constants.INV_ITEM_SIZE[1])))
        
        # Draw rest of inventory
        for row in range(4):
            for item in range(3):
                item_i = 2 + (row * 3) + item
                if self.inventory[item_i] != None:
                    self.inventory[item_i].draw_inv(screen, (inv_location[0] + (item*constants.INV_ITEM_SIZE[0]), inv_location[1] + (row*constants.INV_ITEM_SIZE[1])))
        
        # Draw lives
        temp_surface = pygame.Surface([self.lives * (constants.LIVES_SIZE[0] + 15), constants.LIVES_SIZE[1]], pygame.SRCALPHA) 
        for life in range(self.lives):
            temp_surface.blit(self.lives_texture, [life * (constants.LIVES_SIZE[0] + 15), 0])
        screen.blit(temp_surface, [53, 545])
            
        return screen
    
    def initiate_assets(self, constants):
        self.assets = {}
        # Get sprite-sheet
        master_texture = pygame.image.load(constants.FILE_PATH + "project_lib/assets/player/main.png").convert() # Use text input button design
        images = []
        # Split sprite-sheet into 2d array of images
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

        # SPACE TO ADD MORE ANIMATIONS
