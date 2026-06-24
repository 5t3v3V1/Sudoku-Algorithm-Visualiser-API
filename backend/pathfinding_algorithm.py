from identifier import identify_node
from collections import deque
import heapq

def bfs(grid):
    start_position, end_position = (0, 0), (4, 4)
    grid.append_nodes()
    queue = deque([start_position])
    visited = {start_position}
    visit_order = [start_position]
    nodes_visited = 0
    steps = []

    while queue:
        current = queue.popleft()
        current_node = identify_node(grid, current)
        current_node.visit()
        nodes_visited += 1
        steps.append(grid.to_list())

        if current == end_position:
            path = []

            node = current_node

            while node is not None:
                path.append(node.position)
                node = node.parent

            path.reverse()

            for node_position in path:
                identified_node = identify_node(grid, node_position)
                identified_node.pathed()
                steps.append(grid.to_list())

            bfs_grid = grid  

            return nodes_visited, bfs_grid, steps

        elif current != end_position:
            for neighbour in current_node.get_neighbours():
                neighbour = identify_node(grid, neighbour)
                if neighbour is None:
                    continue

                if neighbour.type != "wall":
                    if neighbour.position not in visited:
                        neighbour.parent = current_node
                        neighbour.visit()
                        visited.add(neighbour.position)
                        visit_order.append(neighbour.position)
                        queue.append(neighbour.position)

    print("Unable to reach desired node")
    return nodes_visited, bfs_grid, steps


def dfs(grid):
    start_position, end_position = (0, 0), (4, 4)
    grid.append_nodes()
    stack = deque([start_position])
    visited = {start_position}
    visit_order = [start_position]
    nodes_visited = 0
    steps = []

    while stack:
        current = stack.pop()
        current_node = identify_node(grid, current)
        current_node.visit()
        nodes_visited += 1
        steps.append(grid.to_list())

        if current == end_position:
            
            path = []

            node = current_node

            while node is not None:
                path.append(node.position)
                node = node.parent

            path.reverse()

            for node_position in path:
                identified_node = identify_node(grid, node_position)
                identified_node.pathed()
                steps.append(grid.to_list())

            dfs_grid = grid 

            return nodes_visited, dfs_grid, steps

        elif current != end_position:
            for neighbour in current_node.get_neighbours():
                neighbour = identify_node(grid, neighbour)
                if neighbour is None:
                    continue

                elif neighbour.type != "wall":
                    if neighbour.position not in visited:
                        neighbour.parent = current_node
                        neighbour.visit()
                        visited.add(neighbour.position)
                        visit_order.append(neighbour.position)
                        stack.append(neighbour.position)

    print("Unable to reach desired node")
    return nodes_visited, dfs_grid, steps

def dijkstra(grid):
    start_position, end_position = (0, 0), (4, 4)
    grid.append_nodes()
    unvisited = set()
    visited = set()
    node_costs_global = {}
    nodes_visited = 0
    start_node = identify_node(grid, start_position)
    start_node.cost = 0
    steps = []
    for row in grid.layout:
        for column in row:
            node_costs_global[column.position] = column.cost
            unvisited.add(column.position)

    while unvisited:
        node_costs = node_costs_global.copy()

        for node in list(node_costs.items()):
            if node[0] in visited:
                node_costs.pop(node[0])

        values = []
        for value in node_costs.values():
            values.append(value)

        heapq.heapify(values)
        min_cost = values[0]

        current = 0

        for node in list(node_costs.items()):
            if node[1] == min_cost:
                current = node[0]

        current_node = identify_node(grid, current)
        current_node.visit()
        nodes_visited += 1
        steps.append(grid.to_list())

        if current == end_position:
            path = []

            node = current_node

            while node is not None:
                path.append(node.position)
                node = node.parent  

            path.reverse()

            for node_position in path:
                identified_node = identify_node(grid, node_position)
                identified_node.pathed()
                steps.append(grid.to_list())

            dijkstra_grid = grid
                 
            return nodes_visited, dijkstra_grid, steps
        
        elif current != end_position:
            for neighbour in current_node.get_neighbours():
                neighbour = identify_node(grid, neighbour)
                if neighbour is None:
                    continue
                
                new_cost = current_node.cost + neighbour.weight

                if neighbour.type != "wall":
                    if new_cost < neighbour.cost:
                        neighbour.parent = current_node
                        neighbour.visit()
                        neighbour.cost = new_cost
                        node_costs[neighbour.position] = neighbour.cost
                        node_costs_global[neighbour.position] = neighbour.cost

            unvisited.discard(current)
            visited.add(current)

    print("Unable to reach desired node")
    return nodes_visited, dijkstra_grid, steps

def astar(grid):
    start_position, end_position = (0, 0), (4, 4)
    grid.append_nodes()
    unvisited = set()
    visited = set()
    node_costs_global = {}
    nodes_visited = 0
    start_node = identify_node(grid, start_position)
    start_node.cost = 0
    start_node.total_cost = 0
    steps = []
    for row in grid.layout:
        for column in row:
            node_costs_global[column.position] = column.total_cost
            unvisited.add(column.position)

    while unvisited:
        node_costs = node_costs_global.copy()

        for node in list(node_costs.items()):
            if node[0] in visited:
                node_costs.pop(node[0])

        values = []
        for value in node_costs.values():
            values.append(value)

        heapq.heapify(values)
        min_cost = values[0]

        current = 0

        for node in list(node_costs.items()):
            if node[1] == min_cost:
                current = node[0]

        current_node = identify_node(grid, current)
        current_node.visit()
        nodes_visited += 1
        steps.append(grid.to_list())

        if current == end_position:
            path = []

            node = current_node

            while node is not None:
                path.append(node.position)
                node = node.parent

            path.reverse()

            for node_position in path:
                identified_node = identify_node(grid, node_position)
                identified_node.pathed()
                steps.append(grid.to_list())

            astar_grid = grid 
                
            return nodes_visited, astar_grid, steps
        
        elif current != end_position:
            for neighbour in current_node.get_neighbours():
                neighbour = identify_node(grid, neighbour)
                if neighbour is None:
                    continue
                
                new_cost = current_node.cost + neighbour.weight
                neighbour.cost_to_end = abs(neighbour.position[0] - end_position[0]) + abs(neighbour.position[1] - end_position[1])
                neighbour.total_cost = neighbour.cost_to_end + new_cost

                if neighbour.type != "wall":
                    if new_cost < neighbour.cost:
                        neighbour.parent = current_node
                        neighbour.cost = new_cost
                        node_costs[neighbour.position] = neighbour.total_cost
                        node_costs_global[neighbour.position] = neighbour.total_cost

            unvisited.discard(current)
            visited.add(current)

    print("Unable to reach desired node")
    return nodes_visited, astar_grid, steps