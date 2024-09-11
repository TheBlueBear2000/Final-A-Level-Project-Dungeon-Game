def get_movement_vector(speed, directionVector):
    if directionVector == [0,0]:
        return directionVector # Return nothing if the vector has no direction
    
    # Calculate original vector distance
    from math import sqrt
    directionDistance = sqrt((directionVector[0] ** 2) + 
			                 (directionVector[1] ** 2))

    # Calculate multiplier
    multiplier = speed / directionDistance
    
    # Multiply axis of original vector by scaler multiplier to scale them correctly
    movementVector = [directionVector[0] * multiplier, 
		      directionVector[1] * multiplier]

    return movementVector
