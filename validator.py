from groups import row_groups, column_groups, box_groups
from identifier import identify_node
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def is_valid(grid, selected_position, number):
    old_value = grid.nodes[selected_position].number
    grid.nodes[selected_position].number = number

    valid = 0
    for group in row_groups:
        valid_numbers_copy = list(valid_numbers)
        if selected_position not in group:
            continue

        else:
            for position in group:
                identified_node = identify_node(grid, position)

                if identified_node.number == 0:
                    continue

                elif identified_node.number in valid_numbers_copy:
                    valid_numbers_copy.remove(identified_node.number)

                elif identified_node.number not in valid_numbers_copy:
                    valid = 1
                    break

    for group in column_groups:
        valid_numbers_copy = list(valid_numbers)
        if selected_position not in group:
            continue

        else:
            for position in group:
                identified_node = identify_node(grid, position)

                if identified_node.number == 0:
                    continue

                elif identified_node.number in valid_numbers_copy:
                    valid_numbers_copy.remove(identified_node.number)

                elif identified_node.number not in valid_numbers_copy:
                    valid = 1
                    break
        
    for group in box_groups:
        valid_numbers_copy = list(valid_numbers)
        if selected_position not in group:
            continue

        else:
            for position in group:
                identified_node = identify_node(grid, position)

                if identified_node.number == 0:
                    continue

                elif identified_node.number in valid_numbers_copy:
                    valid_numbers_copy.remove(identified_node.number)

                elif identified_node.number not in valid_numbers_copy:
                    valid = 1
                    break
              
    if valid == 1:
        grid.nodes[selected_position].number = old_value
        return False
        
    else:
        grid.nodes[selected_position].number = old_value
        return True