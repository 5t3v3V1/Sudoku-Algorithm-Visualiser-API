import random
from backend.validator import is_valid
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def board_generator(board):
    empty_list = list(board.find_zeros())
    if len(empty_list) == 0:
        return True
        
    position = empty_list[0]
    numbers = valid_numbers.copy()
    random.shuffle(numbers)
    for value in numbers:
        if is_valid(board, position, value):
            board.nodes[position].number = value
            if board_generator(board):
                return True
                
            board.nodes[position].number = 0

    return False

def grid_generator():
    possible_nodes = ["#", ".", "?", "~", "^"]
    weights = [0.2, 0.3, 0.25, 0.2, 0.15]
    grid = []

    for h in range(5):
        grid.append("")
        for w in range(5):
            node = random.choices(possible_nodes, weights = weights, k = 1)[0]
            grid[h] += node

    return grid