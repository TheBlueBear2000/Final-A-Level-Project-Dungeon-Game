from math import sqrt
from copy import deepcopy

def a_star(start, end, room, hitbox_size, crates, doors):
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
    end = [int((end[0] - ((constants.GAME_WINDOW_SIZE[0] - room.size[0])//2)) // constants.SQUARE_SIZE[0]), int((end[1] - ((constants.GAME_WINDOW_SIZE[1] - room.size[1])//2)) // constants.SQUARE_SIZE[1])]
    start = [int((start[0] - ((constants.GAME_WINDOW_SIZE[0] - room.size[0])//2)) // constants.SQUARE_SIZE[0]), int((start[1] - ((constants.GAME_WINDOW_SIZE[1] - room.size[1])//2)) // constants.SQUARE_SIZE[1])]
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
                
            if (room.layout[projected_node[1]][projected_node[0]].collidable):
                #print("hit collidable at: " + str(projected_node))
                continue # Dont check collidable nodes
            
            # use pythagoras to find the direct distance between the node and the player location
            nodeHeuristic = sqrt(((projected_node[0] - end[0]) ** 2) +
                                    ((projected_node[1] - end[1]) ** 2))      
            
            nextNodes.append({"value": nodeHeuristic + pathLength,
                                "location": projected_node})
            
        # Compare nodes and find next node 
        #print("start to end:     ", start, " ", end)
        if len(nextNodes) == 0: # if hit a dead end
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
            
            #for check in [[-1,0], [1,0], [0,-1], [0,1]]:
            #    projected_node_tuple = tuple([currentNode[0] + check[0], currentNode[1] + check[1]])
            #    if projected_node_tuple in failed_coordinates and not (projected_node_tuple == lastNode_tuple or projected_node_tuple == path[-2]):
            #        failed_coordinates.remove(projected_node_tuple)
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
    continue_loop = True
    while current_node != path[-1] and continue_loop:
        #print("end node: ", path[-1])
        #print("check")
        for i, node in enumerate(backwards_path):
            if node == current_node:
                if path.index(currentNode) == len(path)-1:
                    continue_loop = False
                    break
                else:
                    new_path.append(path[path.index(currentNode)+1])
                    current_node = path[path.index(currentNode)+1]
                    break
            #print("checking line of sight from ", current_node, " to ", node)
            if line_of_sight([(current_node[0] * constants.SQUARE_SIZE[0]) + room.location[0] + (constants.SQUARE_SIZE[0]//2), (current_node[1] * constants.SQUARE_SIZE[1]) + room.location[1] + (constants.SQUARE_SIZE[1]//2)], 
                            [(node[0] * constants.SQUARE_SIZE[0]) + room.location[0]  + constants.SQUARE_SIZE[0]//2, (node[1] * constants.SQUARE_SIZE[1]) + room.location[1] + constants.SQUARE_SIZE[1]//2], 
                            room, constants, [*crates, *doors], hitbox_size) == "possible":
                #print("there is line of sight from ", current_node, " to ", node)
                #print("end node is ", path[-1])
                new_path.append(node)
                current_node = node
                break
        
            # handle if there is no line of sight between two adjasent nodes
        
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




def line_of_sight(start, end, room, constants, collidables, hitbox_size=[2,2]):
    from functions.algorithms.getMovementVector import get_movement_vector
    from functions.algorithms.collision_detection import is_colliding, collision
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
        
        for collidable in collidables:
            if collision([check[0] - (hitbox_size[0]//2),  check[1] - (hitbox_size[1]//2), *hitbox_size], [*collidable.collision_box["location"], *collidable.collision_box["size"]]):
                return "collidable"

        if is_colliding({"size": hitbox_size, "location": [check[0] - (hitbox_size[0]//2),  check[1] - (hitbox_size[1]//2)]}, room.layout, room.location, constants.SQUARE_SIZE):
            return "wall"
        check = [check[0] + vector[0], check[1] + vector[1]]
        
        #import pygame
        #pygame.draw.rect(screen, (0, 0, 0), (check[0], check[1], 10, 10))
        #print("next location: ", check)
    return "possible" #, screen

def path_possible(loc1, loc2, room_layout):
    # loc1 and 2 as grid coordinates
    
    # searches every square to see if path is possible
    
    current_loc = []
    next_locs = [loc1]
    used_locs = []
    
    while len(next_locs) > 0:
        current_loc = next_locs.pop(0)
        for relative in [[1,0], [-1,0], [0, 1], [0,-1]]:
            to_search = [current_loc[0] + relative[0],  current_loc[1] + relative[1]]
            if to_search[0] >= 0 and to_search[1] >= 0 and to_search[0] < len(room_layout[0]) and to_search[1] < len(room_layout):
                if not (room_layout[to_search[1]][to_search[0]].collidable  or  to_search in used_locs):
                    if loc2 == to_search:
                        return True
                    used_locs.append(to_search)
                    next_locs.append(to_search)
    return False
    





# ALGORITHM CANT FIND PLAYER WHEN PLAYER IS IN COLLIDABLE OBJECT, EVEN WHEN PLAYER IS NOT ACTUALLY COLLIDING WITH IT'S HITBOX. FIND A WAY TO FIX THIS

# SOLUTION: implement line of sight into initial A* algorithm, in order to skip through collidables:
# ISSUE: this will not work when the collidable is in the middle of a path, eg a fence

# SOLUTION: add another boolean for impassable collidables
# ISSUE: if you are within bounding box of non-full, impassable collidable like a fence, then the original issue will occur

# SOLUTION: add booleans for impassable directions (left fences cant be passed left, right fences cant be passed right)
# ISSUE: what do we do with corner fences. If they are both, the original issue will occcur. If they are neither, the algorithm will go through them

# SOLUTION: call all non full collisables as empty. then reassess path afterwards and check line of sight between every node. If it is broken, continue the algorithm from the previous node with the node that was full blacklisted
# ISSUE: all nodes are collidable if approached from 45 degrees. this means that even nodes with tiny collision boxes will be blacklisted even though they are technically passable

# SOLUTION: if player is in collidable, keep track of last non-collidable square and go there instead. Then use line of sight to try to get to the player when within smaller range (1 square)
# ISSUE: very complicated 

# SOLUTION: instead of using grid, use every pixel. This way the algorithm can also navigate around impassable entities such as crates which will not be on layout grid but will be on entity arrays
# ISSUES: may be very inefficient

# SOLUTION: reassess the process for creating collision boxes

# SOLUTION: check line of sight when 1 square away from the player. if there is no line of sight, backstep and blacklist square that cannot see player (sothat path will try to get different angle on the player   )


# SOLUTION: use fill algorithm to check if a path to the player exists. If it doesnt, use remembered last location instead
# now same issue exists but the other way around, where enemy cannot get out of collidable object. 
#   solution: assume that initial location is non collidable, and treat it as such
# that is not the issue. the issue is that when there is only a start and an end, and it's line of sight is blocked while the player is in a collidable, it cannot find alternative routes

# checkpoint testing determined the issue is to do with the initial a* algorithm itself (maybe cant break out of collidable?)

# turns out the issue is with the original algorithm. It is getting stuck in a corner cornered by its own tail. This means that it keeps switching between the surrounding nodes, finding a dead end, backtracing, and then repeating that with another direction till it returns to the last problem
# fixed the issue by removing the code that removes things from the unusable squre list. not sure why i was removing things from there anyway. now it has to backstep till it finds a path

# back to issue to do with line of sight within a square i think. the checkpoint 2 is now the one getting caught
# the issue is not to do with the line of sight algorithm, but the way it is triggered. there is a while loop that keeps triggering it. i will investigate why the loop doesnt break
# it is getting stuck for reason mentioned earlier. The code is unable to find a line of sight between two nodes that are next to eachother, since one is collidable