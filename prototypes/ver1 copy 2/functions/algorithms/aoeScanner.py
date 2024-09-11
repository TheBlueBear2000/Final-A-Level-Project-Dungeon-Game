
from math import sqrt
from classes.global_data import constants_structure

def aoeScanner(origin, entities, room, player, reach, constants, isPlayer = False):
    constants = constants_structure()
    # Python lambda statement to determine if coordinates are within 
    # the radius distance of the origin coordinates
    isInRange = (lambda x, y : sqrt(((origin[0] - x) ** 2) + 
		((origin[1] - y) ** 2)) <= reach)


    # Start with entities
    effectedEntities = []
    for entity in entities:
        if isInRange(entity.collision_box["location"][0] + (entity.collision_box["size"][0]//2), 
                    entity.collision_box["location"][1] + (entity.collision_box["size"][1]//2)):
            effectedEntities.append(entity)

    # Squares
    effectedSquares = []
    for y in range(len(room.layout)):
        for x in range(len(room.layout[y])):
            if isInRange((x * constants.SQUARE_SIZE[0]) + room.location[0], (y * constants.SQUARE_SIZE[1]) + room.location[1]):
                effectedSquares.append([x,y])

    # Player
    playerEffected = False
    if (isInRange(player.collision_box["location"][0] + (player.collision_box["size"][0]//2), 
                    player.collision_box["location"][1] + (player.collision_box["size"][1]//2)) 
                    and not isPlayer):
        playerEffected = True

    return effectedEntities, effectedSquares, playerEffected






