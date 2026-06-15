from validator import is_valid
import time
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def solver(grid):
        empty_list = list(grid.find_zeros())
        if len(empty_list) == 0:
            return True
        
        position = empty_list[0]
        for value in valid_numbers:
            if is_valid(grid, position, value):
                grid.nodes[position].number = value
                if solver(grid):
                    return True
                
                grid.nodes[position].number = 0
            
        return False