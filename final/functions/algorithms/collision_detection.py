def is_colliding(player, room_collidables, room_coordinates, square_size):
    
    # Turn screen coordinates into grid coordinates
    player_grid_x = int((player["location"][0] - room_coordinates[0]) // square_size[0])
    player_grid_y = int((player["location"][1] - room_coordinates[1]) // square_size[1])
    
    # Create a 2x2 2d array of the 4 squares that surround the player. This is calculated by starting from the 
    # coordinate of the player's top-left corner, and then taking the squares directly to the right and below
    # of that coordinate. This instantly removes a lot of squares that do not need to be checked, making the
    # algorithm far more efficient.
    if player_grid_y < len(room_collidables)-1:
        player_surroundings = [ room_collidables[player_grid_y][player_grid_x: player_grid_x + 2],
                                room_collidables[player_grid_y + 1][player_grid_x: player_grid_x + 2]]
    else:
        player_surroundings = [room_collidables[player_grid_y][player_grid_x: player_grid_x + 2]]
        
    # get values for each side of the player
    x1 = player["location"][0]
    y1 = player["location"][1]
    x1_end = player["size"][0]
    y1_end = player["size"][1]
    
    for row in player_surroundings: # Check the 4 connected squares
        for square in row:
            if square.collidable is False: # If the square isn't a collidable, there is no collision
                continue
            # Find values for each side of the square
            x2 = square.collision_x
            y2 = square.collision_y
            x2_end = square.width
            y2_end = square.height
            
            # Check for a collision between the player and the square
            if collision([x1, y1, x1_end, y1_end],  [x2, y2, x2_end, y2_end]):
                return True
            
    return False
    
    
def collision(square_1, square_2):
    # Get sides of both square
    x1 = square_1[0]
    y1 = square_1[1]
    x1_end = x1 + square_1[2]
    y1_end = y1 + square_1[3]
    
    x2 = square_2[0]
    y2 = square_2[1]
    x2_end = x2 + square_2[2]
    y2_end = y2 + square_2[3]
    
    sorted_xs = [x1,x1_end, x2,x2_end]
    sorted_xs.sort() # Sort all X coordinates
    
    # check that both bounding boxes are not next to eachother
    if not (sorted_xs == [x1,x1_end, x2,x2_end] or sorted_xs == [x2,x2_end, x1,x1_end]):  # If squares are overlapping on X
        
        sorted_ys = [y1,y1_end, y2,y2_end]
        sorted_ys.sort() # Sort all Y coordinates
        
        # check that both bounding boxes are not vertically adjasent to eachother
        if not (sorted_ys == [y1,y1_end, y2,y2_end] or sorted_ys == [y2,y2_end, y1,y1_end]):  # If squares are overlapping on Y
            return True # There is a collison since both dimensions are overlapping
    
    # One axis is not overlapping, meaning there is not a coordinate
    return False
