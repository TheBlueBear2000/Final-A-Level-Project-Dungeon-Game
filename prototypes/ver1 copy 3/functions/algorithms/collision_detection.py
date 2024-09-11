

def is_colliding(player, room_collidables, room_coordinates, square_size):
    
    player_grid_x = int((player["location"][0] - room_coordinates[0]) // square_size[0])
    player_grid_y = int((player["location"][1] - room_coordinates[1]) // square_size[1])
    player_surroundings = [ room_collidables[player_grid_y][player_grid_x: player_grid_x + 2],
                            room_collidables[player_grid_y + 1][player_grid_x: player_grid_x + 2]]
    
    x1 = player["location"][0]
    y1 = player["location"][1]
    x1_end = x1 + player["size"][0]
    y1_end = y1 + player["size"][1]
    
    for row in player_surroundings:
        for square in row:
            if square.collidable is False:
                continue
            x2 = square.x_pos
            y2 = square.y_pos
            x2_end = x2 + square.width
            y2_end = y2 + square.height
            
            sorted_xs = [x1,x1_end, x2,x2_end]
            sorted_xs.sort()
            # check that both bounding boxes are not next to eachother
            if not (sorted_xs == [x1,x1_end, x2,x2_end] or sorted_xs == [x2,x2_end, x1,x1_end]): 
                sorted_ys = [y1,y1_end, y2,y2_end]
                sorted_ys.sort()
                # check that both bounding boxes are not vertically adjasent to eachother
                if not (sorted_ys == [y1,y1_end, y2,y2_end] or sorted_xs == [y2,y2_end, y1,y1_end]): 
                    return True
    return False
    
    