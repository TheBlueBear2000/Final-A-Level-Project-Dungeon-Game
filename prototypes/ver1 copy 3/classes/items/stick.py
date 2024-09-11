

import pygame
from classes.item import Item

class StickSword(Item):
    def __init__(self):
        
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        self.type = "stick"
        self.stack_size = 1
        
        self.game_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/items/inv/{self.type}.png").convert()
        self.inv_texture = pygame.image.load(constants.FILE_PATH + f"project_lib/assets/items/inv/{self.type}.png").convert()
        self.mele_damage = 2
        
        
        
        
        
        