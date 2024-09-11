

from classes.entity import Entity
import functions.algorithms.a_star_pathfind as path_finding
from math import sqrt

class Enemy(Entity):
    def __init__(self, x, y, type):
        Entity.__init__(self, x, y, type)
        self.type = type
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
        
    def think(self, player, entities, room, constants):
        
        if self.state == "death":
            if self.animation_frame == len(self.assets["death"])-1:
                return True
            else:
                return False
        if self.state == "spawn":
            if self.animation_frame == len(self.assets["spawn"])-1:
                self.change_state("idle")
            return False
        
    
        # Priority: hunt player, idle
        self.location = self.collision_box["location"]
        player_location = player.collision_box["location"]
        
        # Hunt player if player is within line of sight or has been within 30 ticks
        # player memory:
        if path_finding.line_of_sight([self.location[0] + (self.collision_box["size"][0]//2), self.location[1] + (self.collision_box["size"][1]//2)], player_location, room, constants):
            self.speed = self.run_speed
            self.player_memory = self.max_player_memory
        elif self.player_memory > 0:
            self.speed = self.walk_speed
            self.player_memory -= 1
        
        # if player is being hunted
        if self.player_memory > 0:
            
            if self.attack_cooldown >= 0:
                self.attack_cooldown -= 1
            
            if (self.attack_cooldown <= 0) and (sqrt(((self.x_pos - player.x_pos)**2) + ((self.y_pos - player.y_pos)**2)) < 45):
                self.attack(player, entities, room)
                self.attack_cooldown = self.max_attack_cooldown
            
            if self.attack_timer == 0:
                # Find path to player. I may implement system to reduce use of this algorithm by 
                # only updating it every few ticks unless within closer range of the player
                self.path_to_player = path_finding.a_star(self.location, player_location, room, self.collision_box["size"]) 
                
                
                self.move(self.path_to_player[1], room)
            else:
                self.attack_timer -= 1
            
            # continue code

        else: # idle
            self.speed = self.walk_speed
            
            # ADD PASSIVE WALKING
            
            self.move(self.location, room)
            
            
        return False
            
            
        

