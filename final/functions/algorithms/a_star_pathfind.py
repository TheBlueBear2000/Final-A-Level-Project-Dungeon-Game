from math import sqrt
from copy import deepcopy

def a_star(start, end, room, hitbox_size, crates, doors):
    from classes.global_data import constants_structure
    constants = constants_structure()
    
    # The pathfinding algorithm works in stages:
    
    # Stage 1 - Calculate path from A to B using A* algorithm:
    #           - Attempt path
    #           - If hit a dead end, backstep until a new path can be tried
    
    # Stage 2 - Find shortcuts to shorten path where possible
    
    # Stage 3 - Smooth out path with point to point squares
    
    
    # Define beginning and end (A and B)
    raw_start = deepcopy(start)
    raw_end = deepcopy(end)
    end = [int((end[0] - ((constants.GAME_WINDOW_SIZE[0] - room.size[0])//2)) // constants.SQUARE_SIZE[0]), int((end[1] - ((constants.GAME_WINDOW_SIZE[1] - room.size[1])//2)) // constants.SQUARE_SIZE[1])]
    start = [int((start[0] - ((constants.GAME_WINDOW_SIZE[0] - room.size[0])//2)) // constants.SQUARE_SIZE[0]), int((start[1] - ((constants.GAME_WINDOW_SIZE[1] - room.size[1])//2)) // constants.SQUARE_SIZE[1])]
    
    
    # Stage 1 - A* algorithm:
    pathStartingCoordinates = start
    currentNode = pathStartingCoordinates
    pathLength = 0
    path = [pathStartingCoordinates]
    failed_coordinates = []
    while currentNode != end: # Keep trying until path is complete
        nextNodes = []
        pathLength += 1
        for check in [[-1,0], [1,0], [0,-1], [0,1]]: # Check neighboring squares
            # Get projected coordinate
            projected_node = [currentNode[0] + check[0], currentNode[1] + check[1]]
            projected_node_tuple = tuple(projected_node)

            if projected_node_tuple in failed_coordinates:
                continue # Skip that node it if is failed (we know it leads to a dead end)
            
            if (projected_node[0] < 0 or
                projected_node[0] > len(room.layout[0]) or
                projected_node[1] < 0 or
                projected_node[1] > len(room.layout)):
                continue # Dont check past room boundries
                
            if (room.layout[projected_node[1]][projected_node[0]].collidable):
                continue # Dont check collidable nodes
            
            # use pythagoras to find the direct distance between the node and the player location (the heuristic)
            nodeHeuristic = sqrt(((projected_node[0] - end[0]) ** 2) +
                                    ((projected_node[1] - end[1]) ** 2))      
            
            # Add node to list
            nextNodes.append({"value": nodeHeuristic + pathLength,
                                "location": projected_node})
            
        # Compare nodes and find next node 
        
        if len(nextNodes) == 0: # If there are no more paths found, the square is a dead end
            if len(path) == 0:
                # No more nodes to backtrack, path is not possible
                return None
            if len(path) == 1:
                return [raw_start, raw_end]
            # Remove the last node from the path
            lastNode = path.pop()
            pathLength -= 1
            failed_coordinates.append(tuple(currentNode))
            currentNode = path[-1]
            
        else: # If not a dead end
            closestNode = nextNodes[0]
            for node in nextNodes[1:]:
                # Set the closest node to whichever node has the smallest value
                closestNode = closestNode if closestNode["value"] < node["value"] else node 
            
            # Add node to path
            path.append(closestNode["location"])
            currentNode = closestNode["location"]
            
            # If coordinate is reached again, algorithm will go in a circle which will cause an endless loop
            failed_coordinates.append(tuple(currentNode)) 
    
    
    # Stage 2 - Shortcuts:
    if len(path) == 1: # If the path is only one item long, return it
        return [raw_start, raw_end]
    
    # find shortcuts in the path
    # from the start of the path, traverse every node and work from the end to find one that is next to it
    # if it is next to a node that is several nodes ahead in the path list, then all nodes inbetween can be removed since a shortcut has been found
    new_shortcut = True
    new_path = path
    while new_shortcut:
        path = new_path
        new_shortcut = False
        for i, node in enumerate(path): # Check along the path 
            backwards_path = path[i + 2:]
            backwards_path.reverse() # Check along the path backwards
            for back_i, back_node in enumerate(backwards_path):
                # check surroundings
                for check in [[-1,0], [1,0], [0,-1], [0,1]]:
                    projected_node_tuple = tuple([node[0] + check[0], node[1] + check[1]])
                    if projected_node_tuple == tuple(back_node):
                        new_path = path[:i+1] + path[len(path)-back_i-1:]
                        new_shortcut = i != len(path) - back_i
    # Update path
    path = new_path
    
    
    # Stage 3 - Path smoothing
    
    # Now smooth path into minimum number of points, allowing overlap
    # Do this by starting at first node, and working backwards from last node until there is direct line of sight (will require line of sight function)
    # Then put the further line of sight node next to the start node in a new faster path
    # repeat again, starting from the new furthest node, until there is line of sight to the end location
    
    # Make copies of the path forwards and backwards
    new_path = [path[0]]
    current_node = path[0]
    backwards_path = deepcopy(path)
    backwards_path.reverse()
    continue_loop = True
    while current_node != path[-1] and continue_loop: # Until the path reaches the end
        for i, node in enumerate(backwards_path): # Move backwards through the path to find furthest direct node
            if node == current_node:
                if path.index(currentNode) == len(path)-1:
                    continue_loop = False
                    break
                else:
                    new_path.append(path[path.index(currentNode)+1])
                    current_node = path[path.index(currentNode)+1]
                    break
            
            # Check line if sight to that node
            if line_of_sight([(current_node[0] * constants.SQUARE_SIZE[0]) + room.location[0] + (constants.SQUARE_SIZE[0]//2), (current_node[1] * constants.SQUARE_SIZE[1]) + room.location[1] + (constants.SQUARE_SIZE[1]//2)], 
                            [(node[0] * constants.SQUARE_SIZE[0]) + room.location[0]  + constants.SQUARE_SIZE[0]//2, (node[1] * constants.SQUARE_SIZE[1]) + room.location[1] + constants.SQUARE_SIZE[1]//2], 
                            room, constants, [*crates, *doors], hitbox_size) == "possible":
                new_path.append(node)
                current_node = node # Continue checking from the new node, since nodes between the old and new one can be removed
                break
    # Update path
    path = new_path
    
        
    # Turn all nodes in path from grid coordinates to screen coordinates
    path = [[((node[0]+0.5) * constants.SQUARE_SIZE[0]) + room.location[0], 
            ((node[1]+0.5) * constants.SQUARE_SIZE[1]) + room.location[1]]  for node in path]
    
    return path


def line_of_sight(start, end, room, constants, collidables, hitbox_size=[2,2]):
    from functions.algorithms.getMovementVector import get_movement_vector
    from functions.algorithms.collision_detection import is_colliding, collision
    # use a ray-tracing algorithm to check every few pixels directly between the two nodes
    
    # Create particle data
    check = start
    total_vector = [end[0] - start[0], end[1] - start[1]]
    vector = get_movement_vector(3 , total_vector)
    
    while sqrt(((check[0]-end[0])**2) + ((check[1]-end[1])**2)) > 5:
        # Check if particle has collided with collidable entities
        for collidable in collidables:
            if collision([check[0] - (hitbox_size[0]//2),  check[1] - (hitbox_size[1]//2), *hitbox_size], [*collidable.collision_box["location"], *collidable.collision_box["size"]]):
                return "collidable"

        # Check if particle has collided with squares
        if is_colliding({"size": hitbox_size, "location": [check[0] - (hitbox_size[0]//2),  check[1] - (hitbox_size[1]//2)]}, room.layout, room.location, constants.SQUARE_SIZE):
            return "wall"
        
        # If there has not been a collision, move particle
        check = [check[0] + vector[0], check[1] + vector[1]]
        
    return "possible" # if particle reaches destination without colliding, return that the line of sight exists

def path_possible(loc1, loc2, room_layout):
    # loc1 and loc2 parameters should be given as grid coordinates
    
    # Searches every square to see if path is possible
    
    current_loc = []
    next_locs = [loc1]
    used_locs = []
    
    # Use a depth-first search (using a queue) to search all surrounding squares to see if two squares are connected by non-colliding squares
    # If they are connected, then a path could be calculated between the two points. Otherwise, the path may be impossible
    while len(next_locs) > 0:
        current_loc = next_locs.pop(0)
        for relative in [[1,0], [-1,0], [0, 1], [0,-1]]:
            to_search = [current_loc[0] + relative[0],  current_loc[1] + relative[1]]
            if to_search[0] >= 0 and to_search[1] >= 0 and to_search[0] < len(room_layout[0]) and to_search[1] < len(room_layout):
                if not (room_layout[to_search[1]][to_search[0]].collidable  or  to_search in used_locs):
                    if loc2 == to_search:
                        return True # If the destination has been reached, return true
                    used_locs.append(to_search)
                    next_locs.append(to_search)
                    
    # If queue is completely empty, the all nodes have been checked and points are not connected
    return False
