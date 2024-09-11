
from classes.entities.enemy import Enemy
from classes.global_data import constants_structure
from random import randint

class Goblin(Enemy):
    def __init__(self, x, y, health, room_loc):
        Enemy.__init__(self, x, y, "goblin", room_loc)
        import json
        constants = constants_structure()
        # Extract data
        data = json.load(open(constants.FILE_PATH + "data/entities/enemies/goblin.json", "r"))
        self.max_health = data["health"]
        
        self.health = health
        if health == -1: # -1 means default
            self.health = self.max_health
            
        self.walk_speed = data["walk_speed"]
        self.run_speed = data["run_speed"]
        self.max_player_memory = randint(data["max_player_memory_range"][0], data["max_player_memory_range"][1])
        self.size = data["size"]
        self.collision_box["size"] = data["collision_box_size"]
        self.team = data["team"]
        self.mele_reach = data["mele_reach"]
        self.attack_damage = data["attack_damage"]
        self.max_attack_cooldown = data["attack_cooldown"]
        
        