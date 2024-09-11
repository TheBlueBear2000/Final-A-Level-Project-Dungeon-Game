

def lookup(name):
    the_class = None
    if name == "goblin":
        from classes.entities.enemies.goblin import Goblin
        the_class = Goblin
    
    elif name == "crate":
        from classes.entities.moveable_squares.crate import Crate
        the_class = Crate

    elif name == "item":
        from classes.items.living_item import LivingItem
        the_class = LivingItem
        
        
    return the_class


