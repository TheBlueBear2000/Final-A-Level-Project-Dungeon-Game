import json
import copy

class Room:
    def __init__(self, data):
        from classes.square import Square
        from classes.global_data import constants_structure
        constants = constants_structure()
        
    
        
        self.layout = []
        squares_data = json.load(open(constants.FILE_PATH + "data/squares/squares_data.json", "r"))
        default_square = json.load(open(constants.FILE_PATH + "data/squares/default_square.json", "r"))
        
        self.size = [len(data["squares"][0]) * constants.SQUARE_SIZE[0], len(data["squares"]) * constants.SQUARE_SIZE[1]]
        self.location = ((constants.DEFAULT_SCREEN_SIZE[0] - self.size[0]) // 2, (constants.DEFAULT_SCREEN_SIZE[1] - self.size[1]) // 2) 
        
        for y, row in enumerate(data["squares"]):
            new_row = [None for _ in range(len(row))]
            for x, square in enumerate(row):
                new_row[x] = Square(squares_data[square], default_square, constants.FILE_PATH, constants.SQUARE_SIZE, [self.location[0] + (x * constants.SQUARE_SIZE[0]), self.location[1] + (y * constants.SQUARE_SIZE[1])])
            self.layout.append(new_row)
        
        
        
    #     for row in data["squares"]:
    #         new_row = [None for _ in range(len(row))]
    #         for i, square in enumerate(row):
    #             new_square = self.fill_square(copy.deepcopy(squares_data[square]), default_square)
    #             new_row[i] = new_square
    #         self.layout.append(new_row)
            
    # def fill_square(self, square, default):
    #     out_data = copy.deepcopy(default)
    #     for data in square:
    #         out_data[data] = square[data]
    #     #print("in:  " + str(square))
    #     #print("out: " + str(out_data))
    #     return out_data
    
    def draw(self, screen, square_size):
        for y, row in enumerate(self.layout):
            for x, square in enumerate(row):
                screen = square.draw(screen, self.location[0] + (square_size[0] * x), self.location[1] + (square_size[1] * y))
        return screen