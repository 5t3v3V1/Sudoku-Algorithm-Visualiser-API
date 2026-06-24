from backend.validator import is_valid
import time
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def solver(grid, steps = None, moves = None):
        if steps is None:
            steps = []
            moves = 0

        empty_list = list(grid.find_zeros())
        if len(empty_list) == 0:
            return True, steps, moves
        
        position = empty_list[0]
        for value in valid_numbers:
            if is_valid(grid, position, value):
                grid.nodes[position].number = value
                steps.append(grid.to_list())
                moves += 1
                solved, steps = solver(grid, steps, moves)
                if solved:
                    return True, steps, moves
                
                grid.nodes[position].number = 0
                steps.append(grid.to_list())
                moves += 1
            
        return False, steps, moves