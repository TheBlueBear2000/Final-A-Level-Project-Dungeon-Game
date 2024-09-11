

def is_colliding(player, room_collidables, room_coordinates, square_size):
    
    player_grid_x = int((player["location"][0] - room_coordinates[0]) // square_size[0])
    player_grid_y = int((player["location"][1] - room_coordinates[1]) // square_size[1])
    if player_grid_y < len(room_collidables)-1:
        player_surroundings = [ room_collidables[player_grid_y][player_grid_x: player_grid_x + 2],
                                room_collidables[player_grid_y + 1][player_grid_x: player_grid_x + 2]]
    else:
        player_surroundings = [room_collidables[player_grid_y][player_grid_x: player_grid_x + 2]]
        
    
    x1 = player["location"][0]
    y1 = player["location"][1]
    x1_end = player["size"][0]
    y1_end = player["size"][1]
    
    for row in player_surroundings:
        for square in row:
            if square.collidable is False:
                continue
            x2 = square.collision_x
            y2 = square.collision_y
            x2_end = square.width
            y2_end = square.height
            
            if collision([x1, y1, x1_end, y1_end],  [x2, y2, x2_end, y2_end]):
                return True
            
    #print("not collision")
    return False
    
    
def collision(square_1, square_2):
    x1 = square_1[0]
    y1 = square_1[1]
    x1_end = x1 + square_1[2]
    y1_end = y1 + square_1[3]
    
    x2 = square_2[0]
    y2 = square_2[1]
    x2_end = x2 + square_2[2]
    y2_end = y2 + square_2[3]
    
    sorted_xs = [x1,x1_end, x2,x2_end]
    sorted_xs.sort()
    # check that both bounding boxes are not next to eachother
    if not (sorted_xs == [x1,x1_end, x2,x2_end] or sorted_xs == [x2,x2_end, x1,x1_end]): 
        sorted_ys = [y1,y1_end, y2,y2_end]
        sorted_ys.sort()
        # check that both bounding boxes are not vertically adjasent to eachother
        if not (sorted_ys == [y1,y1_end, y2,y2_end] or sorted_ys == [y2,y2_end, y1,y1_end]): 
            #print("collision")
            #print("collision between: \n", square_1, ",\n", square_2, "\n\n")
            return True

    return False