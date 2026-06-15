from pydantic import BaseModel

class SudokuRequest(BaseModel):
    board: list[list[int]]

class Grid:
    def __init__(self, layout):
        self.nodes = {}
        self.layout = layout.copy()
        self.reset_layout = layout.copy()
    
    def append_positions(self):
        for row_index, row in enumerate(self.layout):
            row_items = list(row)
            for index, item in enumerate(row_items):
                self.nodes[(index, row_index)] = Node(item, (index, row_index))

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
            row = []

            for x in range(9):
                row.append(self.nodes[(x, y)].number)

            board.append(row)

        return board

class Node:
    def __init__(self, number, position):
        self.number = number
        self.position = position