from math import sqrt
from copy import deepcopy

def a_star(start, end, room, hitbox_size):
    from classes.global_data import constants_structure
    constants = constants_structure()
    # at this point, room squares are either 0 for non-collidable or 1 for collidable

    # self is the enemy, since the function is contained by the enemy class
    # room is the room layout, a 2d array of squares
    # end is the coordinates of the player (2 item array of floats for x and y coordinates)
    
    # I will be implementing a variation of the A* pathfinding algorithm that operates
    # on a 2d grid, where the nodes look as per the attatched diagram (fig 3.1)
    # DRAW DIAGRAM ^
    
    # This algorithm will be used to generate a vague path, and then another algorithm will be ran which smooths the path out
    # It does this by splitting the path into straight horizontal and/or vertical parts
    # It then creates a point at the center of where these parts connect
    # This results in direct travel between two points, rather than a path being very rough and jaggedy
    # This then becomes a straight line from the player to that node
    # The algorithm is then repeated, with that new node as the target, until the enemy has a direct view of a node, at which point the shortest path has been found
    # This algorithm is not very efficient, but it provides a very good result
    # On large scale, this algorithm can look rough and inefficient, but on a small scale it should work smoothly
    # Taken from: https://gamedev.stackexchange.com/questions/81593/a-star-pathfinding-and-discrete-smooth-positions
    # ^ MAKE REFERENCE
    
    
    # end = [int(coord + 0.5) for coord in end] # Rounds both coordinates to the nearest whole number. But this might make the enemy go past the player since it will look at the top left corner
    # Rounds the coordinates to a whole number, but whichever is closest to the enemy, to prevent the algorithm searching past the player
    #real_end = end
    #real_start = start
    #print("start: ", start)
    #print("end:   ", end)
    raw_start = deepcopy(start)
    raw_end = deepcopy(end)
    end = [int((end[0] - ((constants.DEFAULT_SCREEN_SIZE[0] - room.size[0])//2)) // constants.SQUARE_SIZE[0]), int((end[1] - ((constants.DEFAULT_SCREEN_SIZE[1] - room.size[1])//2)) // constants.SQUARE_SIZE[1])]
    start = [int((start[0] - ((constants.DEFAULT_SCREEN_SIZE[0] - room.size[0])//2)) // constants.SQUARE_SIZE[0]), int((start[1] - ((constants.DEFAULT_SCREEN_SIZE[1] - room.size[1])//2)) // constants.SQUARE_SIZE[1])]
    #end = [(int(coord) if coord < start[i] else int(coord + 1)) for i, coord in enumerate(end)] 
    #print("start after translation:  ", start)
    
    #print()
    
    # A* algorithm:
    # Same expression as above, to find the closest rounding to the player from the enemy
    #pathStartingCoordinates = [(int(coord) if coord < end[i] else int(coord + 1)) for i, coord in enumerate(start)]
    pathStartingCoordinates = start
    currentNode = pathStartingCoordinates
    pathLength = 0
    path = [pathStartingCoordinates]
    failed_coordinates = []
    while currentNode != end:
        # Check all nodes around currentNode
        nextNodes = []
        pathLength += 1
        for check in [[-1,0], [1,0], [0,-1], [0,1]]:
            projected_node = [currentNode[0] + check[0], currentNode[1] + check[1]]
            projected_node_tuple = tuple(projected_node)

            if projected_node_tuple in failed_coordinates:
                continue
            
            if (projected_node[0] < 0 or
                projected_node[0] > len(room.layout[0]) or
                projected_node[1] < 0 or
                projected_node[1] > len(room.layout)):
                continue # Dont check past room boundries
                
            if room.layout[projected_node[1]][projected_node[0]].collidable:
                #print("hit collidable at: " + str(projected_node))
                continue # Dont check collidable nodes
            
            # use pythagoras to find the direct distance between the node and the player location
            nodeHeuristic = sqrt(((projected_node[0] - end[0]) ** 2) +
                                    ((projected_node[1] - end[1]) ** 2))      
            
            nextNodes.append({"value": nodeHeuristic + pathLength,
                                "location": projected_node})
            
        # Compare nodes and find next node 
        #print("start to end:     ", start, " ", end)
        if len(nextNodes) == 0:
            if len(path) == 0:
                # No more nodes to backtrack, path is not possible
                return None
            if len(path) == 1:
                return [raw_start, raw_end]
            # Remove the last node from the path
            lastNode = path.pop()
            pathLength -= 1
            currentNode = path[-1]
            lastNode_tuple = tuple(lastNode)
            failed_coordinates.append(lastNode_tuple)
            for check in [[-1,0], [1,0], [0,-1], [0,1]]:
                projected_node_tuple = tuple([currentNode[0] + check[0], currentNode[1] + check[1]])
                if projected_node_tuple in failed_coordinates and not (projected_node_tuple == lastNode_tuple or projected_node_tuple == path[-2]):
                    failed_coordinates.remove(projected_node_tuple)
        else:

            closestNode = nextNodes[0]
            for node in nextNodes[1:]:
                closestNode = closestNode if closestNode["value"] < node["value"] else node # Set the closest node to whichever node has the smallest value
            
            # add node to list, and begin searching from it
            #print("start node is: " + str(pathStartingCoordinates))
            #print("end node is: " + str(end))
            #print("adding: " + str(closestNode["location"]))
            #print()
            path.append(closestNode["location"])
            currentNode = closestNode["location"]
            
            failed_coordinates.append(tuple(currentNode))
    
    # Post A* algorithm:    
    
    if len(path) == 1:
        return [raw_start, raw_end]
    
    # find shortcuts in the path
    # from the start of the path, traverse every node and work from the end to find one that is next to it
    new_shortcut = True
    new_path = path
    while new_shortcut:
        path = new_path
        new_shortcut = False
        for i, node in enumerate(path):
            backwards_path = path[i + 2:]
            backwards_path.reverse()
            for back_i, back_node in enumerate(backwards_path):
                # check surroundings
                for check in [[-1,0], [1,0], [0,-1], [0,1]]:
                    projected_node_tuple = tuple([node[0] + check[0], node[1] + check[1]])
                    if projected_node_tuple == tuple(back_node):
                        new_path = path[:i+1] + path[len(path)-back_i-1:]
                        new_shortcut = i != len(path) - back_i
    path = new_path
    
    
    
    
    # Now smooth path into minimum number of points, allowing overlap#
    # Do this by starting at first node, and working backwards from last node until there is direct line of sight (will require line of sight function)
    # Then put the further line of sight node next to the start node in a new faster path
    # repeat again, starting from the new furthest node, until there is line of sight to the end location
    
    #   print(path)
    
    #path[0] = real_start
    #path[-1] = real_end
    
    #path = [real_start] + deepcopy(path)[1:-2] + [real_end]
    
    new_path = [path[0]]
    current_node = path[0]
    backwards_path = deepcopy(path)
    backwards_path.reverse()
    #print("current node: ", current_node)
    #print(len(path))
    #print(len(path)-1)
    #print(path)
    while current_node != path[-1]:
        #print("end node: ", path[-1])
        #print("check")
        for i, node in enumerate(backwards_path):
            #print("checking line of sight from ", current_node, " to ", node)
            if line_of_sight([(current_node[0] * constants.SQUARE_SIZE[0]) + room.location[0] + (constants.SQUARE_SIZE[0]//2), (current_node[1] * constants.SQUARE_SIZE[1]) + room.location[1] + (constants.SQUARE_SIZE[1]//2)], 
                            [(node[0] * constants.SQUARE_SIZE[0]) + room.location[0]  + constants.SQUARE_SIZE[0]//2, (node[1] * constants.SQUARE_SIZE[1]) + room.location[1] + constants.SQUARE_SIZE[1]//2], 
                            room, constants, hitbox_size):
                #print("there is line of sight from ", current_node, " to ", node)
                #print("end node is ", path[-1])
                new_path.append(node)
                current_node = node
                break
                #if current_node == path[-1]:
                #    break
    path = new_path
    
        
        
    path = [[((node[0]+0.5) * constants.SQUARE_SIZE[0]) + room.location[0], 
            ((node[1]+0.5) * constants.SQUARE_SIZE[1]) + room.location[1]]  for node in path]
    
    #print(path)
    #print(real_start)
    #print(real_end)
    #print()
    #path = [real_start] + deepcopy(path)[1:-2] + [real_end]
    return path
    # currentBox = []
    # currentDirectionVector = [int(path[0][0] - pathStartingCoordinates[0]), int(path[0][1] - pathStartingCoordinates[1])]

    # for i, node in enumerate(path[:-1]):
    #     nextCurrentDirectionVector = [int(path[i+1][0] - path[i][0]), int(path[i+1][1] - path[i][1])]
    #     if nextCurrentDirectionVector != currentDirectionVector:
    #         switchPoints.append([])   




def line_of_sight(start, end, room, constants, hitbox_size=[2,2]):
    from functions.algorithms.getMovementVector import get_movement_vector
    from functions.algorithms.collision_detection import is_colliding
    # use a raytracing algorithm to check every few pixels directly between the two nodes
    check = start
    total_vector = [end[0] - start[0], end[1] - start[1]]
    vector = get_movement_vector(3 , total_vector)
    #print("checking from ", start, " to ", end, " with vector ", vector)
    #vector = [-1 * vector[0], -1 * vector[1]]
    #print(sqrt(((check[0]-end[0])**2) + ((check[1]-end[1])**2)))
    while sqrt(((check[0]-end[0])**2) + ((check[1]-end[1])**2)) > 5:
    #while check != end:
        #print(check)
        #print("start: ", start)
        #print("end: ", end)
        #print("total vector: ", total_vector)
        #print("vector: ", vector)
        #print("checking: ", check)
        #check_coords = [(check[0] * constants.SQUARE_SIZE[0]) + room.location[0], (check[1] * constants.SQUARE_SIZE[1]) + room.location[1]]
        if is_colliding({"size": hitbox_size, "location": [check[0] - (hitbox_size[0]//2),  check[1] - (hitbox_size[1]//2)]}, room.layout, room.location, constants.SQUARE_SIZE):
            #print("collision")
            return False
        check = [check[0] + vector[0], check[1] + vector[1]]
        
        #import pygame
        #pygame.draw.rect(screen, (0, 0, 0), (check[0], check[1], 10, 10))
        #print("next location: ", check)
    
    return True#, screen



