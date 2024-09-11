def lookup(name):
    the_class = None
    
    if name == "stick":
        from classes.items.items import StickSword
        the_class = StickSword
        
    # Wooden armour
    elif name == "wood_head":
        from classes.items.items import WoodenHelmet
        the_class = WoodenHelmet
    elif name == "wood_chest":
        from classes.items.items import WoodenChestplate
        the_class = WoodenChestplate
    elif name == "wood_feet":
        from classes.items.items import WoodenBoots
        the_class = WoodenBoots
        
    # Chainmail armour
    elif name == "chain_head":
        from classes.items.items import ChainmailHelmet
        the_class = ChainmailHelmet
    elif name == "chain_chest":
        from classes.items.items import ChainmailChestplate
        the_class = ChainmailChestplate
    elif name == "chain_feet":
        from classes.items.items import ChainmailBoots
        the_class = ChainmailBoots
    
    # Metal armour
    elif name == "metal_head":
        from classes.items.items import IronHelmet
        the_class = IronHelmet
    elif name == "metal_chest":
        from classes.items.items import IronChestplate
        the_class = IronChestplate
    elif name == "metal_feet":
        from classes.items.items import IronBoots
        the_class = IronBoots
        
    # Mele weapons
    elif name == "long_sword":
        from classes.items.items import LongSword
        the_class = LongSword
    elif name == "metal_axe":
        from classes.items.items import Axe
        the_class = Axe
    elif name == "dagger":
        from classes.items.items import Dagger
        the_class = Dagger
    elif name == "mace":
        from classes.items.items import Mace
        the_class = Mace
        
    # Misc
    elif name == "key":
        from classes.items.items import Key
        the_class = Key
    
    # SPACE TO ADD NEW ITEMS
        
    return the_class
