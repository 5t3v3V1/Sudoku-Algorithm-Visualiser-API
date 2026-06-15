import random
from validator import is_valid
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