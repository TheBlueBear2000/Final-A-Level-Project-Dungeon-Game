import json
import pygame

class Room:
    def __init__(self, data, level):
        from classes.square import Square
        from classes.special_squares.door import Door
        from classes.special_squares.mechanical_door import MechanicalDoor
        from classes.special_squares.objective_door import ObjectiveDoor
        from classes.entities.moveable_squares.crate import Crate
        from classes.special_squares.button import Button
        from classes.special_squares.lever import Lever
        from classes.special_squares.ladder import Ladder
        from classes.special_squares.keyhole_wall import Keyhole
        
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        self.level = level
        
        self.kills = 0
        
        # Squares
        
        self.layout = []
        self.doors = []
        self.crates = []
        self.buttons = []
        self.levers = []
        self.ladder = None
        
        squares_data = json.load(open(constants.FILE_PATH + "data/squares/squares_data.json", "r"))
        default_square = json.load(open(constants.FILE_PATH + "data/squares/default_square.json", "r"))
        
        self.size = [len(data["squares"][0]) * constants.SQUARE_SIZE[0], len(data["squares"]) * constants.SQUARE_SIZE[1]]
        self.location = ((constants.GAME_WINDOW_SIZE[0] - self.size[0]) // 2, (constants.GAME_WINDOW_SIZE[1] - self.size[1]) // 2) 
        
        for y, row in enumerate(data["squares"]):
            new_row = [None for i in range(len(row))]
            for x, square in enumerate(row):
                square_int = False
                if isinstance(square, int):
                    square_int = True
                if square_int  and  squares_data[square]["basic"]:
                    size = constants.SQUARE_SIZE
                    if "size" in squares_data[square]:
                        size = [constants.SQUARE_SIZE[0] * squares_data[square]["size"][0], constants.SQUARE_SIZE[1] * squares_data[square]["size"][1]]
                    new_row[x] = Square(squares_data[square], default_square, constants.FILE_PATH, size, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])

                else:
                    if isinstance(square, int):
                        square_name = squares_data[square]["name"]
                    else:
                        square_name = (squares_data[square["id"]]["name"])
                    
                    if square_name.endswith("door"):
                        # DOORS
                        new_row[x] = Square(squares_data[0], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
                        if square["pos"][1] == "t":
                            corner = "top_"
                        else:
                            corner = "bottom_"
                        if square["pos"][2] == "l":
                            corner += "left"
                        else:
                            corner += "right"
                            
                        if square_name.startswith("mechanical"):
                            print("open" in square)
                            self.doors.append(MechanicalDoor(x, y, corner, square["pos"][0], self.location, square["colour"], is_open=(square["open"] if "open" in square else False)))
                        
                        elif square_name.startswith("keyhole"):
                            print("open" in square)
                            self.doors.append(MechanicalDoor(x, y, corner, square["pos"][0], self.location, square["colour"], "keyhole", is_open=(square["open"] if "open" in square else False)))
                            
                        else:
                            self.doors.append(Door(x, y, corner, square["pos"][0], self.location))
                    
                    elif square_name.startswith("button"):
                        # BUTTONS
                        new_row[x] = Square(squares_data[0], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
                        self.buttons.append(Button(square["colour"], (x,y), self.location))
                    
                    elif square_name.startswith("lever"):
                        # LEVERS
                        new_row[x] = Square(squares_data[0], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
                        flicked = False
                        if "flicked" in square:
                            flicked = square["flicked"]
                        self.levers.append(Lever(square["colour"], flicked, (x,y), self.location))
                    
                    elif square_name == "crate":
                        # CRATE
                        new_row[x] = Square(squares_data[0], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
                        self.crates.append(Crate(x, y, self.location))
                    
                    elif square_name == "ladder":
                        # LADDER
                        new_row[x] = Square(squares_data[0], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
                        self.ladder = Ladder(x, y, self.location)
                    
                    elif square_name == "keyhole_wall":
                        # KEYHOLE
                        new_row[x] = Keyhole(x, y, self.location, square["colour"])
                        #self.crates.append(Crate(x, y, self.location))
                        
            
            self.layout.append(new_row)
            
        
        
        
        # Entities
        from functions.algorithms.item_lookup import lookup as i_lookup
        from functions.algorithms.entity_lookup import lookup as e_lookup
        self.entities = []
        self.living_items = []
        
        for entity in data["entities"]:
            entity_class = e_lookup(entity["name"])
            if entity["name"] == "crate":
                self.crates.append(entity_class(entity["x"], entity["y"], self.location))
                continue
            elif entity["name"] == "item": 
                self.living_items.append(entity_class(entity["x"], entity["y"], i_lookup(entity["item"])(entity["payload"])))
                continue
            health = -1
            if "health" in entity:
                health = entity["health"]
            drops = {}
            if "drops" in entity:
                drops = entity["drops"]
            self.entities.append(entity_class(entity["x"], entity["y"], health, self.location, drops))
            
        
        self.active_colours = {}
        for trigger in [*self.levers, *self.buttons]:
            self.active_colours[str(trigger.colour)] = False
            
        self.id = data["id"]
        self.objectives = data["doors"]
        
        # update the way that data["doors"] and self.gates works so that the value is either None, 
        # meaning no door, or a string that corresponds to an objective. The objectives can then 
        # be checked, and different doors should be designed that can only be opened by room objectives:
        
        # for objective in self.objectives:
        #     if self.objectives[objective] is not None:
        
        self.objective_doors = []
        self.objective_icons = []
        from classes.objective_icon import ObjectiveIndicator
        for objective in self.objectives:
            if self.objectives[objective] is not None:
                self.objective_icons.append(ObjectiveIndicator(objective, self.objectives[objective]))
                if not ("colour" in self.objectives[objective]):
                    self.objectives[objective]["colour"] = None
        
        non_navigable_air = Square(squares_data[7], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
        if self.objectives["left"] is not None:
            self.layout[len(self.layout)//2-1][0] = non_navigable_air
            self.layout[len(self.layout)//2][0] = non_navigable_air
            if self.objectives["left"]["type"] != "empty":
                self.objective_doors.append(self.objective_door_generate(self.objectives["left"]["type"], 0, len(self.layout)//2-1, "top_right", "v", self.objectives["left"]["colour"], "left"))
                self.objective_doors.append(self.objective_door_generate(self.objectives["left"]["type"], 0, len(self.layout)//2, "bottom_right", "v", self.objectives["left"]["colour"], "left"))
            
        if self.objectives["right"] is not None:
            self.layout[len(self.layout)//2-1][len(self.layout[0])-1] = non_navigable_air
            self.layout[len(self.layout)//2][len(self.layout[0])-1] = non_navigable_air
            if self.objectives["right"]["type"] != "empty":
                self.objective_doors.append(self.objective_door_generate(self.objectives["right"]["type"], len(self.layout[0])-1, len(self.layout)//2-1, "top_left", "v", self.objectives["right"]["colour"], "right"))
                self.objective_doors.append(self.objective_door_generate(self.objectives["right"]["type"], len(self.layout[0])-1, len(self.layout)//2, "bottom_left", "v", self.objectives["right"]["colour"], "right"))
            
        if self.objectives["up"] is not None:
            self.layout[0][len(self.layout[0])//2-1] = non_navigable_air
            self.layout[0][len(self.layout[0])//2] = non_navigable_air
            if self.objectives["up"]["type"] != "empty":
                self.objective_doors.append(self.objective_door_generate(self.objectives["up"]["type"], len(self.layout[0])//2-1, 0, "bottom_left", "h", self.objectives["up"]["colour"], "up"))
                self.objective_doors.append(self.objective_door_generate(self.objectives["up"]["type"], len(self.layout[0])//2, 0, "bottom_right", "h", self.objectives["up"]["colour"], "up"))
            
        if self.objectives["down"] is not None:
            self.layout[len(self.layout)-1][len(self.layout[0])//2-1] = non_navigable_air
            self.layout[len(self.layout)-1][len(self.layout[0])//2] = non_navigable_air
            if self.objectives["down"]["type"] != "empty":
                self.objective_doors.append(self.objective_door_generate(self.objectives["down"]["type"], len(self.layout[0])//2-1, len(self.layout)-1, "top_left", "h", self.objectives["down"]["colour"], "down"))
                self.objective_doors.append(self.objective_door_generate(self.objectives["down"]["type"], len(self.layout[0])//2, len(self.layout)-1, "top_right", "h", self.objectives["down"]["colour"], "down"))
                
        for door in self.objective_doors:
            if self.objectives[door.side]["complete"]:
                door.open()
            elif self.objectives[door.side]["type"] == "empty":
                self.complete_objective(door.side)
                
        
        
        
        #elif square_name.startswith("objective"):
        #   self.objective_doors.append(ObjectiveDoor(x, y, corner, square["pos"][0], self.location, square["objective"], square["colour"]))
        #   new_row[x] = Square(squares_data[7], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])], [x,y])
            
        #for objective in data.doors:
        
        
        
    def objective_door_generate(self, objective_type, x, y, hinge_corner, starting_dir, colour=None, side = None):   
        if objective_type == "keyhole":
            from classes.special_squares.mechanical_door import MechanicalDoor
            return MechanicalDoor(x, y, hinge_corner, starting_dir, self.location, colour, "keyhole", side)
        elif objective_type == "powered":
            from classes.special_squares.mechanical_door import MechanicalDoor
            return MechanicalDoor(x, y, hinge_corner, starting_dir, self.location, colour, objective_side = side)
        else:
            from classes.special_squares.objective_door import ObjectiveDoor
            return ObjectiveDoor(x, y, hinge_corner, starting_dir, self.location, colour, side)
        
        
    def complete_objective(self, objective_side):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        # set objective to complete
        self.objectives[objective_side]["complete"] = True
        
        if objective_side == "left":
            objective_opposite = "right"
        elif objective_side == "right":
            objective_opposite = "left"
        elif objective_side == "up":
            objective_opposite = "down"
        else:
            objective_opposite = "up"
        
        level_layout = json.load(open(constants.FILE_PATH + f"data/levels/rooms_{self.level}/layout.json", 'r'))
        
        # find next room
        next_room_id = None
        for y, row in enumerate(level_layout):
            for x, item in enumerate(row):
                if item == self.id:
                    if objective_side == "left":
                        next_room_id = level_layout[y][x-1]
                    elif objective_side == "right":
                        next_room_id = level_layout[y][x+1]
                    elif objective_side == "up":
                        next_room_id = level_layout[y-1][x]
                    elif objective_side == "down":
                        next_room_id = level_layout[y+1][x]
                
        # update next room
        
        with open(constants.FILE_PATH + f"data/levels/rooms_{self.level}/{next_room_id}.json", 'r') as file:
            data = json.load(file)
        data["doors"][objective_opposite]["complete"] = True
            
        with open(constants.FILE_PATH + f"data/levels/rooms_{self.level}/{next_room_id}.json", 'w') as file:
            json_string = json.dumps(data)
            file.write(json_string)
        
        # open doors
        for door in self.objective_doors:
            if door.side == objective_side:
                door.open()
    
    def update(self, player):
        for colour in self.active_colours:
            self.active_colours[colour] = False
        
        for lever in self.levers:
            if lever.flicked:
                self.active_colours[str(lever.colour)] = True
        for button in self.buttons:
            if not button.state_up:
                self.active_colours[str(button.colour)] = True
                
        for door in self.doors:
            if not door.manual and door.type == "button":
                if str(door.colour) in self.active_colours:
                    if self.active_colours[str(door.colour)]:
                        door.open()
                    else:
                        door.close()
                    #door.open = self.active_colours[str(door.colour)]
                    
                    
        # Special door objectives
        for objective in self.objectives:
            if self.objectives[objective] is not None:
                if not self.objectives[objective]["complete"]:
                    # Kill count:
                    if self.objectives[objective]["type"] == "kill_count":
                        if player.kills >= self.objectives[objective]["num"]:
                            self.complete_objective(objective)
                            
                    elif self.objectives[objective]["type"] == "local_kill_count":
                        if self.kills >= self.objectives[objective]["num"]:
                            self.complete_objective(objective)
                            
                    # No enemies:
                    # if self.objectives[objective]["type"] == "kill_count":
                    #     if player.kills >= self.objectives[objective]["num"]:
                    #         self.complete_objective(objective)
                    
                    # Powered
                    elif self.objectives[objective]["type"] == "powered":
                        if self.active_colours[str(self.objectives[objective]["colour"])]:
                            self.complete_objective(objective)
                    
                    # Keyhole is done elsewhere
                
        
    
    def save(self):
        data = {"id": self.id,
                "doors": self.objectives}
        
        # basic squares
        squares = []
        for y, row in enumerate(self.layout):
            new_row = []
            for x, square in enumerate(row):
                new_row.append(square.save())
            squares.append(new_row)
        # overlay buttons, levers and doors
        for lever in self.levers:
            squares[lever.grid_location[1]][lever.grid_location[0]] = lever.save()
        for button in self.buttons:
            squares[button.grid_location[1]][button.grid_location[0]] = button.save()
        for door in self.doors:
            squares[door.grid_location[1]][door.grid_location[0]] = door.save()
        
        # ladder
        if self.ladder is not None:
            squares[self.ladder.grid_coords[1]][self.ladder.grid_coords[0]] = 10
        
        data["squares"] = squares
        
        # entities
        entities = []
        
        for entity in self.entities:
            entities.append(entity.save(self.location))
            
        for crate in self.crates:
            entities.append(crate.save(self.location))
            
        for item in self.living_items:
            entities.append(item.save(self.location))
        
        data["entities"] = entities
        
        
        from classes.global_data import constants_structure
        constants = constants_structure()
        with open(constants.FILE_PATH + f"data/levels/rooms_{self.level}/{self.id}.json", 'w') as file:
            json_string = json.dumps(data)
            file.write(json_string)
            #json.dump(data, file, indent=4)
            
    def get_rendering_list(self):
        rendering_list = []
        for row in self.layout:
            for item in row:
                rendering_list.append(item)
        rendering_list += [*self.buttons, *self.levers, *self.doors, *self.objective_doors, *self.entities, *self.living_items, *self.crates]
        if self.ladder is not None:
            rendering_list.append(self.ladder)
            
        return(rendering_list)
            
    
    def draw(self, screen, square_size, config):
        from classes.global_data import constants_structure
        constants = constants_structure()
        # draw base, later should calculate connected textures too
        # will also need extra room layout later to extablish different squares
        #print(self.location[0]-constants.SQUARE_SIZE[0])
        #tunnels
        tunnel = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/menu/tunnel_h.png").convert(), (square_size[0] * 3, square_size[1] * 4.5))
        if self.objectives["right"] is not None:
            screen.blit(tunnel, (self.location[0] + self.size[0], (constants.GAME_WINDOW_SIZE[1] - tunnel.get_height())//2 - (constants.SQUARE_SIZE[1]//4)))
        if self.objectives["left"] is not None:
            screen.blit(tunnel, (self.location[0] - tunnel.get_width(), (constants.GAME_WINDOW_SIZE[1] - tunnel.get_height())//2 - (constants.SQUARE_SIZE[1]//4)))
            
        tunnel = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/menu/tunnel_v.png").convert(), (square_size[0] * 4, square_size[1] * 3.5))
        #if self.objectives["down"] is not None:
        #    screen.blit(tunnel, ((constants.GAME_WINDOW_SIZE[0] - tunnel.get_width())//2,  self.location[1] + self.size[1] - (constants.SQUARE_SIZE[1]//4)))
        if self.objectives["up"] is not None:
            screen.blit(tunnel, ((constants.GAME_WINDOW_SIZE[0] - tunnel.get_width())//2,  self.location[1] - tunnel.get_height()))
        
        # base
        for y, row in enumerate(self.layout):
            for x, square in enumerate(row):
                texture = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/squares/ground.png").convert(), square_size)
                screen.blit(texture, (self.location[0] + (square_size[0] * x), self.location[1] + (square_size[1] * y)))
                #screen.blit(self.textures[0], (x_loc, y_loc))
        
        
        # draw squares
        for y, row in enumerate(self.layout):
            for x, square in enumerate(row):
                screen = square.draw(screen)
        
        
        # for button in self.buttons:
        #     screen = button.draw(screen)
        # for lever in self.levers:
        #     screen = lever.draw(screen)
        # for door in [*self.doors, *self.objective_doors]:
        #     screen = door.draw(screen)
            
        # for entity in self.entities:
        #     screen = entity.draw(screen, config["max_FPS"])
        
        # for item in self.living_items:
        #     screen = item.draw(screen)
        
        # for crate in self.crates:
        #     screen = crate.draw(screen)
            
        # if self.ladder is not None:
        #     screen = self.ladder.draw(screen)
        
        
        return screen
    
    def draw_over(self, screen, square_size):
        from classes.global_data import constants_structure
        constants = constants_structure()
        
        tunnel = pygame.transform.scale(pygame.image.load(constants.FILE_PATH + "project_lib/assets/menu/tunnel_v.png").convert(), (square_size[0] * 4, square_size[1] * 3.5))
        
        if self.objectives["down"] is not None:
            screen.blit(tunnel, ((constants.GAME_WINDOW_SIZE[0] - tunnel.get_width())//2,  self.location[1] + self.size[1] - (constants.SQUARE_SIZE[1]//2)))
    
        return screen
    
    def draw_icons(self, screen, player):
        
        
        for icon in self.objective_icons:
            text = ""
            if self.objectives[icon.side]["type"] == "kill_count":
                text = f"{min(self.objectives[icon.side]['num'], player.kills)}/{self.objectives[icon.side]['num']}"
            elif self.objectives[icon.side]["type"] == "local_kill_count":
                text = f"{min(self.objectives[icon.side]['num'], self.kills)}/{self.objectives[icon.side]['num']}"
            elif self.objectives[icon.side]["type"] == "keyhole":
                text = "LOCKED"
                if self.objectives[icon.side]["complete"]:
                    text = "UNLOCKED"
            elif self.objectives[icon.side]["type"] == "powered":
                text = "OFF"
                if self.objectives[icon.side]["complete"]:
                    text = "ON"
            screen = icon.draw(screen, text)
        return screen
        
    
    