from pydantic import BaseModel

class SudokuRequest(BaseModel):
    board: list[list[int]]

class GridRequest(BaseModel):
    grid: list[str]

class Board:
    def __init__(self, layout):
        self.nodes = {}
        self.layout = layout.copy()
        self.reset_layout = layout.copy()
    
    def append_positions(self):
        for row_index, row in enumerate(self.layout):
            row_items = list(row)
            for index, item in enumerate(row_items):
                self.nodes[(index, row_index)] = Board_Node(item, (index, row_index))

    def find_zeros(self):
        empty = {}
        for node in list(self.nodes.items()):
            if node[1].number == 0:
                empty[node[0]] = node[1].number
        
        return empty
    
    def reset(self):
        self.layout = self.reset_layout.copy()
        self.nodes = {}

    def to_list(self):
        board = []
        for y in range(9):
            row = ""

            for x in range(9):
                row += str(self.nodes[(x, y)].number)

            board.append(row)

        return board

class Board_Node:
    def __init__(self, number, position):
        self.number = number
        self.position = position


class Grid:
    def __init__(self, layout):
        self.layout = layout.copy()
        self.nodes = {}
        self.reset_layout = layout.copy()
    
    def append_nodes(self):
        for row_index, row in enumerate(self.layout):
            row_items = list(row)
            for index, item in enumerate(row_items):
                if (index, row_index) in [(0, 0), (4, 4)]:
                    node = Grid_Node("node", (index, row_index), 1, False)
    
                elif item == "#":
                    node = Grid_Node("wall", (index, row_index), 0, False)
                    
                elif item == ".":
                    node = Grid_Node("node", (index, row_index), 1, False)
                    
                elif item == "?":
                    node = Grid_Node("node", (index, row_index), 5, False)
                    
                elif item == "~":
                    node = Grid_Node("node", (index, row_index), 10, False)
                   
                elif item == "^":
                    node = Grid_Node("node", (index, row_index), 15, False)
                    
                self.nodes[(index, row_index)] = node
                row_items[index] = node
            
            self.layout[row_index] = row_items

        return self.layout         
    
    def reset(self):
        self.layout = self.reset_layout.copy()
        self.nodes = {}

    def to_list(self):
        grid = []
        for y in self.layout:
            row = ""
            for x in y:
                if x.path == True:
                    row += "*"

                elif x.visited == True:
                    row += "!"

                elif x.weight == 15:
                    row += "^"

                elif x.weight == 10:
                    row += "~"

                elif x.weight == 5:
                    row += "?"

                elif x.weight == 1:
                    row += "."

                elif x.weight == 0:
                    row += "#"
                    
            grid.append(row)

        return grid

class Grid_Node:
    def __init__(self, type, position, weight, visited):
        self.type = type
        self.position = position
        self.visited = visited
        self.weight = weight
        self.parent = None
        self.path = False
        self.cost = float("inf")
        self.cost_to_end = 0
        self.total_cost = float("inf")

    def get_neighbours(self):
        x, y = self.position
        return [(x, y - 1),
                (x - 1, y),
                (x, y + 1),
                (x + 1, y)
                ]
    
    def visit(self):
        self.visited = True
        self.type = "visited_node"
    
    def pathed(self):
        self.path = True