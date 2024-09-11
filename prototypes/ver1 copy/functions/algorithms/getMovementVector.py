

def get_movement_vector(speed, directionVector):
    if directionVector == [0,0]:
        return directionVector
    # Calculate direction vector distance
    from math import sqrt
    directionDistance = sqrt((directionVector[0] ** 2) + 
			                 (directionVector[1] ** 2))

    # Calculate multiplier
    multiplier = speed / directionDistance
    
    movementVector = [directionVector[0] * multiplier, 
		      directionVector[1] * multiplier]

    return movementVector




#getMovementVector = lambda speed, directionVector : [distance * (speed / (sqrt((directionVector[0] ** 2) + (directionVector[1] ** 2))))  for distance in directionVector]


