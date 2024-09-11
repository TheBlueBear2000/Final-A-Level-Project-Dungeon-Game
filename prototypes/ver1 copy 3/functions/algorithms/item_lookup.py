

def lookup(name):
    the_class = None
    if name == "stick_sword":
        from classes.items.stick import StickSword
        the_class = StickSword
        
    return the_class