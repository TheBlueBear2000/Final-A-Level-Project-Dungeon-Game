from classes.entity import Entity
import functions.algorithms.a_star_pathfind as path_finding
from math import sqrt

class Enemy(Entity): # Enemy class extends Entity
    def __init__(self, x, y, type, room_loc, drops):
        # Initiate object as an Entity
        Entity.__init__(self, x, y, type, room_loc, drops)
        
        # Set default attributes (inheriting classes will change these in their constructors)
        self.player_memory = 0
        self.max_player_memory = 45
        self.run_speed = 4
        self.walk_speed = 2
        self.idle_destination = []
        self.team = "enemy"
        self.attack_damage = 5
        self.max_attack_cooldown = 30
        self.attack_cooldown = self.max_attack_cooldown
        self.attack_frame = 0
        self.player_remembered_location = [x, y] # temporary, till replaced
        
    def think(self, player, entities, crates, doors, room, constants):
        
        # Check for frozen states (enemy doesn't do any other processing when spawning or dying)
        if self.state == "death":
            if self.animation_frame == len(self.assets["death"])-1:
                return True
            else:
                return False
        if self.state == "spawn":
            if self.animation_frame == len(self.assets["spawn"])-1:
                self.change_state("idle")
            return False
        
    
        # Priority order: attack, hunt player, wander, idle
        self.location = self.collision_box["location"]
        
        player_location = player.collision_box["location"] # Get player real location
            
        from functions.algorithms.a_star_pathfind import path_possible
        
        
        # Hunt player if player is within line of sight or has been within enemy memory time
        
        # Check if player is in line of sight
        LOS_result = path_finding.line_of_sight([self.location[0] + (self.collision_box["size"][0]//2), self.location[1] + (self.collision_box["size"][1]//2)], player_location, room, constants, [*crates, *doors])
        if LOS_result == "possible":
            # Check if path to player is possible
            if path_possible(self.get_square(room), player.get_square(room), room.layout): # check if path to player possible
                # If player is being hunted and path is possible, update remembered location
                self.player_remembered_location = player_location # if it is, update memory. If it is not, then memory will not be updated and will therefore be the same
            # Set enemy to be hunting 
            self.speed = self.run_speed
            self.player_memory = self.max_player_memory
            
        elif self.player_memory > 0:
            # If enemy is not hunting, set to wandering and begin to reduce memory
            self.speed = self.walk_speed
            self.player_memory -= 1
        
        # If player is being hunted
        if self.player_memory > 0:
            
            if self.attack_cooldown >= 0:
                self.attack_cooldown -= 1
            
            # If player can be attacked, do the attack
            if (self.attack_cooldown <= 0) and (sqrt(((self.x_pos - player.x_pos)**2) + ((self.y_pos - player.y_pos)**2)) < 45):
                self.attack(player, entities, room)
                self.attack_cooldown = self.max_attack_cooldown
            
            
            # If enemy is not attacking, continue to chase player
            if self.attack_timer == 0:
                
                self.path_to_player = path_finding.a_star(self.location, self.player_remembered_location, room, self.collision_box["size"], crates, doors) 
                
                # Path is an array of direct points to player location. Carry out path
                if len(self.path_to_player) > 1:
                    self.move(self.path_to_player[1], room, crates, doors)
                else:
                    self.move(self.player_remembered_location, room, crates, doors)
            else:
                self.attack_timer -= 1
            
            

        else: # idle
            self.speed = self.walk_speed
            
            # SPACE TO ADD PASSIVE WALKING FEATURE
            
            self.move(self.location, room, crates, doors)
            
            
        return False
            
