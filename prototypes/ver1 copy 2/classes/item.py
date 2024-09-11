

import pygame

class Item:
    
    def draw_inv(self, screen, location):
        
        from classes.global_data import constants_structure, draw_text
        constants = constants_structure()
        
        temp_surface = pygame.Surface(constants.INV_ITEM_SIZE, pygame.SRCALPHA) # Creating translucent shapes requires a custom surface to be created that can take in Alpha colours
        temp_surface.blit(pygame.transform.scale(self.inv_texture, (constants.INV_ITEM_SIZE[0] - 24, constants.INV_ITEM_SIZE[1] - 24)),(12,12))
        screen.blit(temp_surface, location)
        
        return screen
        
        