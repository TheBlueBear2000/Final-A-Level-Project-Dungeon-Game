

import pygame
from classes.item import Item

# All items have their own small class with its own individual details
# Creating a new item is as easy as adding a new class and setting the details correctly. The game handles the rest

# ARMOUR
# Wooden Armour
class WoodenHelmet(Item):
    def __init__(self, payload):
        
        # Define data
        self.type = "wood_head"
        self.name = "Wooden Helmet"
        
        # Initiate self as item
        Item.__init__(self, self.type)
        
        self.sort = "helmet"
        
        # Set multipliers
        self.speed_multiplier = 0.9
        self.mele_armour_multiplier = 0.95
        
class WoodenChestplate(Item):
    def __init__(self, payload):
        
        self.type = "wood_chest"
        self.name = "Wooden Chestplate"
        
        Item.__init__(self, self.type)
        
        self.sort = "chestplate"
        
        self.speed_multiplier = 0.85
        self.mele_armour_multiplier = 0.9
        
class WoodenBoots(Item):
    def __init__(self, payload):
        
        self.type = "wood_feet"
        self.name = "Wooden Boots"
        
        Item.__init__(self, self.type)
        
        self.sort = "boots"
        
        self.speed_multiplier = 0.9
        self.mele_armour_multiplier = 0.95

# Chainmail Armour
class ChainmailHelmet(Item):
    def __init__(self, payload):
        
        self.type = "chain_head"
        self.name = "Chainmail Helmet"
        
        Item.__init__(self, self.type)
        
        self.sort = "helmet"
        
        self.speed_multiplier = 0.85
        self.mele_armour_multiplier = 0.97
        self.ranged_armour_multiplier = 0.95
        
class ChainmailChestplate(Item):
    def __init__(self, payload):
        
        self.type = "chain_chest"
        self.name = "Chainmail Chestplate"
        
        Item.__init__(self, self.type)
        
        self.sort = "chestplate"
        
        self.speed_multiplier = 0.8
        self.mele_armour_multiplier = 0.95
        self.ranged_armour_multiplier = 0.92
        
class ChainmailBoots(Item):
    def __init__(self, payload):
        
        self.type = "chain_feet"
        self.name = "Chainmail Boots"
        
        Item.__init__(self, self.type)
        
        self.sort = "boots"
        
        self.speed_multiplier = 0.85
        self.mele_armour_multiplier = 0.97
        self.ranged_armour_multiplier = 0.95
        
# Iron Armour
class IronHelmet(Item):
    def __init__(self, payload):
        
        self.type = "metal_head"
        self.name = "Iron Helmet"
        
        Item.__init__(self, self.type)
        
        self.sort = "helmet"
        
        self.speed_multiplier = 0.8
        self.mele_armour_multiplier = 0.9
        self.ranged_armour_multiplier = 0.83
        
class IronChestplate(Item):
    def __init__(self, payload):
        
        self.type = "metal_chest"
        self.name = "Iron Chestplate"
        
        Item.__init__(self, self.type)
        
        self.sort = "chestplate"
        
        self.speed_multiplier = 0.7
        self.mele_armour_multiplier = 0.85
        self.ranged_armour_multiplier = 0.75
        
class IronBoots(Item):
    def __init__(self, payload):
        
        self.type = "metal_feet"
        self.name = "Iron Boots"
        
        Item.__init__(self, self.type)
        
        self.sort = "boots"
        
        self.speed_multiplier = 0.8
        self.mele_armour_multiplier = 0.9
        self.ranged_armour_multiplier = 0.8
        

# WEAPONS
class StickSword(Item):
    def __init__(self, payload):
        
        self.type = "stick"
        self.name = "Stick"
        
        Item.__init__(self, self.type)
        
        self.sort = "mele"
        
        self.damage_multiplier = 2
        
class LongSword(Item):
    def __init__(self, payload):
        
        self.type = "long_sword"
        self.name = "Long Sword"
        
        Item.__init__(self, self.type)
        
        self.sort = "mele"
        
        self.damage_multiplier = 3.5
        self.attack_speed_multiplier = 0.9
        self.mele_range_multiplier = 1.2

class Axe(Item):
    def __init__(self, payload):
        
        self.type = "metal_axe"
        self.name = "Axe"
        
        Item.__init__(self, self.type)
        
        self.sort = "mele"
        
        self.damage_multiplier = 5
        self.attack_speed_multiplier = 0.5
        self.mele_range_multiplier = 1.2
        
class Dagger(Item):
    def __init__(self, payload):
        
        self.type = "dagger"
        self.name = "Dagger"
        
        Item.__init__(self, self.type)
        
        self.sort = "mele"
        
        self.damage_multiplier = 2.5
        self.attack_speed_multiplier = 2.5
        self.mele_range_multiplier = 0.7
        
class Mace(Item):
    def __init__(self, payload):
        
        self.type = "mace"
        self.name = "Mace"
        
        Item.__init__(self, self.type)
        
        self.sort = "mele"
        
        self.damage_multiplier = 2
        self.attack_speed_multiplier = 0.75
        self.mele_range_multiplier = 2
        

class Key(Item):
    def __init__(self, payload):
        
        self.type = "key"
        self.name = "Key"
        self.colour = payload["colour"]
        
        Item.__init__(self, self.type, payload)
        
        self.sort = "tool"
        
        # Texture is shaded according to colour data
        temp_surface = pygame.Surface((self.inv_texture.get_width(), self.inv_texture.get_height()), pygame.SRCALPHA)
        temp_surface.blit(self.inv_texture, (0,0))
        temp_surface.fill(self.colour, special_flags=pygame.BLEND_MULT)
        self.inv_texture = temp_surface
        self.game_texture = temp_surface
    
    def save(self): # Save method is overridden since payload contains more data
        return {
            "item": self.type, 
            "payload": {"colour": self.colour}
            }
    
    
# SPACE TO ADD MORE ITEMS LATER

