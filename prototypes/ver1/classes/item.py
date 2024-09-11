

import pygame

class Item:
    def __init__(self, type, payload=None):
        # Armour
        self.speed_multiplier = 1
        self.mele_armour_multiplier = 1
        self.ranged_armour_multiplier = 1
        # Mele
        self.damage_multiplier = 1
        self.attack_speed_multiplier = 1
        self.mele_range_multiplier = 1
        # Ranged
        self.ranged_reload_multiplier = 1
        # Charms
        self.max_health_multiplier = 1
        self.regen_speed = 0 # How much is added every tick to the regen speed timer (when timer is more than 1, it adds 1 health and resets to 0). Items do not add regen by default. Only works for charms
        self.stamina_recharge_multiplier = 1
        
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        self.sort = "generic"
        self.type = type
        self.payload = payload
        self.game_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/items/{type}.png").convert()
        self.inv_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/items/{type}.png").convert()
        
    
    def draw_inv(self, screen, location):
        
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        temp_surface = pygame.Surface(constants.INV_ITEM_SIZE, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(pygame.transform.scale(self.inv_texture, (constants.INV_ITEM_SIZE[0] - 24, constants.INV_ITEM_SIZE[1] - 24)),(12,12))
        screen.blit(temp_surface, location)
        
        return screen
        
        
    def save(self):
        return {
            "item": self.type, 
            "payload": None
            }
        