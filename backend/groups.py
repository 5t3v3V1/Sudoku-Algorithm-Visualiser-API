def append_groups():
    row_groups = []
    column_groups = []
    box_groups = []

    for row in range(9):
        row_groups.append([])
        for column in range(9):
            row_groups[row].append((column, row))

    for column in range(9):
        column_groups.append([])
        for row in range(9):
            column_groups[column].append((column, row))

    for box_row in range(0, 9, 3):
        for box_column in range(0, 9, 3):

            box = []

            for y in range(box_row, box_row + 3):
                for x in range(box_column, box_column + 3):
                    box.append((x, y))

            box_groups.append(box)

    return row_groups, column_groups, box_groups

row_groups, column_groups, box_groups = append_groups()