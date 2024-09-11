

from classes.entity import Entity
import functions.algorithms.a_star_pathfind as path_finding
from math import sqrt

class Enemy(Entity):
    def __init__(self, x, y, type, room_loc, drops):
        Entity.__init__(self, x, y, type, room_loc, drops)
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
        
        #if not room.layout[player.get_square(room)[1]][player.get_square(room)[0]].collidable:
            
        from functions.algorithms.a_star_pathfind import path_possible
        
        
        # Hunt player if player is within line of sight or has been within 30 ticks
        # player memory:
        LOS_result = path_finding.line_of_sight([self.location[0] + (self.collision_box["size"][0]//2), self.location[1] + (self.collision_box["size"][1]//2)], player_location, room, constants, [*crates, *doors])
        if LOS_result == "possible":
            if path_possible(self.get_square(room), player.get_square(room), room.layout): # check if path to player possible
                self.player_remembered_location = player_location # if it is, update memory. If it is not, then memory will not be updated and will therefore be the same
            self.speed = self.run_speed
            self.player_memory = self.max_player_memory
            # check if path to player is possible. if it is, run algorithm, otherwise run algorithm to last remembered location
            #print (player.get_square(room))
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
                #print(self.player_remembered_location)
                #print(player_location)
                #print()
                self.path_to_player = path_finding.a_star(self.location, self.player_remembered_location, room, self.collision_box["size"], crates, doors) 
                
                #print(self.path_to_player)
                if len(self.path_to_player) > 1:
                    self.move(self.path_to_player[1], room, crates, doors)
                else:
                    self.move(self.player_remembered_location, room, crates, doors)
            else:
                self.attack_timer -= 1
            
            # continue code

        else: # idle
            self.speed = self.walk_speed
            
            # ADD PASSIVE WALKING
            
            self.move(self.location, room, crates, doors)
            
            
        return False
            
            
        

