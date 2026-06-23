# Algorithm Visualiser

## What is it

This is a full stack visualiser containing the backend logic for a sudoku solver, BFS, DFS, Dijkstra and A* pathfinding algorithms. Using FastAPI, it contains endpoints to generate or solve boards and grids, and then endpoints to generate and solve grids and boards. The frontend has a vanilla JS version aswell as a react version. The react frontend is deployed on vercel while the backend is deployed on render.

Vercel: https://algorithm-visualiser-api.vercel.app/

## Algorithms Implemented

Sudoku Solver
Creates a list from the find_zeros method of the grid, and then using this list, it picks out the first coordinate with a 0 value, and by using the is_valid function it goes through every valid value, changes the number at the position, then recurces until solver returns true which is when there are no longer any zeros left on the board, if solver returns false though, it backtracks and repeats.

Board Generator
Using an all 0 predefined board, using the same logic as solver(), producing a uniquely valid board on every run, 40 numbers are then removed
from it at random to provide the puzzle.

Grid Generator
Allows the user to input the desired width and height of the grid they want to generate, then lays out the possible nodes and the proabbilities they 
have of showing up before, creating the an array called grid, which is where the layout will live, and creates a new string "" the number of times there is height and
for each string appends a random node type the width number of times, before returning the finished layout.

BFS
Creates a queue containing the start position, it then pops out the first index of the queue, checks whether its the end position, if not it finds all of it's neighbours,
adds them to the queue if they havent already been visited, and repeats until the end position is reached.

DFS
Operates very similar, in the case it does the exact same checks, but instead of a queue, it uses a stack, meaning when instead of popping the first index of the array it pops the last.

Dijkstra
Continiously picks out the node with the smallest cost, removes node from a copy of dicitonary containing all psoitions and their costs, finds the neigbhbours, assigns
new costs by using the nieghbour's weight, and then repeat until end node is reached.

A*
Similar to Dijkstra's but picks out the node with the smallest total cost, containing their cost and the cost to the end, removes node from a copy of the dictionary
containing all positions and their costs, finds the neighbours, assigns the number a new total cost by finding its cost to the end aswell as the cost to get to it, and 
then repeats until the end node is reached

