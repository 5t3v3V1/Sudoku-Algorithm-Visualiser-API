from validator import is_valid
import time
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def solver(grid, steps = None):
        if steps is None:
            steps = []

        empty_list = list(grid.find_zeros())
        if len(empty_list) == 0:
            return True, steps
        
        position = empty_list[0]
        for value in valid_numbers:
            if is_valid(grid, position, value):
                grid.nodes[position].number = value
                steps.append(grid.to_list())
                solved, steps = solver(grid, steps)
                if solved:
                    return True, steps
                
                grid.nodes[position].number = 0
                steps.append(grid.to_list())
            
        return False, steps