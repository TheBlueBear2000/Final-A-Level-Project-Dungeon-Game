from math import sqrt
from classes.global_data import constants_structure

def aoeScanner(origin, entities, room, player, reach, constants, isPlayer = False):
    constants = constants_structure()
    
    # Python lambda statement to determine if a set of coordinates are within the radius distance of the origin coordinate
    isInRange = (lambda x, y, the_reach : sqrt(((origin[0] - x) ** 2) + ((origin[1] - y) ** 2)) <= the_reach)


    # Check each entity
    effectedEntities = []
    for entity in entities:
        if isInRange(entity.collision_box["location"][0] + (entity.collision_box["size"][0]//2), 
                    entity.collision_box["location"][1] + (entity.collision_box["size"][1]//2), reach):
            effectedEntities.append(entity)

    # Check each square
    effectedSquares = []
    for y in range(len(room.layout)):
        for x in range(len(room.layout[y])):
            # Check every corner of the square seperatley
            if (isInRange((x * constants.SQUARE_SIZE[0]) + room.location[0], (y * constants.SQUARE_SIZE[1]) + room.location[1], reach - 20) or # top left
                isInRange((x * constants.SQUARE_SIZE[0]) + room.location[0] + constants.SQUARE_SIZE[0], (y * constants.SQUARE_SIZE[1]) + room.location[1], reach - 20) or # top right
                isInRange((x * constants.SQUARE_SIZE[0]) + room.location[0], (y * constants.SQUARE_SIZE[1]) + room.location[1] + constants.SQUARE_SIZE[1], reach - 20) or # bottom left
                isInRange((x * constants.SQUARE_SIZE[0]) + room.location[0] + constants.SQUARE_SIZE[0], (y * constants.SQUARE_SIZE[1]) + room.location[1] + constants.SQUARE_SIZE[1], reach - 20)):  # bottom right
                effectedSquares.append([x,y])

    # Player
    playerEffected = False # There is only one player, so the player being effected is a boolean
    if (isInRange(player.collision_box["location"][0] + (player.collision_box["size"][0]//2), 
                    player.collision_box["location"][1] + (player.collision_box["size"][1]//2), reach) 
                    and not isPlayer):
        playerEffected = True

    return effectedEntities, effectedSquares, playerEffected
