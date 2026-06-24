from fastapi import FastAPI
from pydantic import BaseModel
from solver import solver
import random
import copy
import time
from validator import is_valid
from classes import Board, SudokuRequest, Grid, Grid_Node, GridRequest
from generator import board_generator, grid_generator
from pathfinding_algorithm import bfs, dfs, dijkstra, astar
from fastapi.middleware.cors import CORSMiddleware
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://algorithm-visualiser-api.vercel.app"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def message():
    return {
        "message": "Algorithm Visualiser API"
    }

@app.get("/health")
def health():
    return {
        "status": "online"
    }

@app.get("/generate_grid")
def generate_grid():
    grid = grid_generator()

    return {
        "grid": grid
    }

@app.get("/generate_board")
def generate_board():
    board = [[], [], [], [], [], [], [], [], []]
    for y in range(9):
        for x in range(9):
            board[y].append(0)

    board = Board(board)
    board.append_positions()

    board_generator(board)

    positions = list(board.nodes.keys())

    random.shuffle(positions)

    for position in positions[:40]:
        board.nodes[position].number = 0

    return {
        "board": board.to_list()
    }

@app.get("/generate_solve_board")
def generate_solve_board():
    board = [[], [], [], [], [], [], [], [], []]
    for y in range(9):
        for x in range(9):
            board[y].append(0)

    board = Board(board)
    board.append_positions()

    board_generator(board)

    positions = list(board.nodes.keys())

    random.shuffle(positions)

    for position in positions[:40]:
        board.nodes[position].number = 0

    generated_board = copy.deepcopy(board)

    start = time.perf_counter()
    
    solved, board_steps = solver(board)

    end = time.perf_counter()

    if not solved:
        return {
            "solved": solved,
            "board": board.to_list(),
            "error": "Board is unsolvable"
        }

    return {
        "solved": solved,
        "generated_board": generated_board.to_list(),
        "board_steps": board_steps,
        "solved_board": board.to_list(),
        "time_ms": (end - start) * 1000
    }

@app.get("/generate_solve_grid")
def generate_solve_grid():
    grid = grid_generator()
    generated_grid = grid.copy()
    generated_grid = Grid(generated_grid)
    generated_grid.append_nodes()

    bfs_grid = Grid(grid)
    dfs_grid = Grid(grid)
    dijkstra_grid = Grid(grid)
    astar_grid = Grid(grid)
    
    bfs_start = time.perf_counter()
    bfs_nodes, solved_bfs_grid, bfs_steps = bfs(bfs_grid)
    bfs_end = time.perf_counter()

    dfs_start = time.perf_counter()
    dfs_nodes, solved_dfs_grid, dfs_steps = dfs(dfs_grid)
    dfs_end = time.perf_counter()

    dijkstra_start = time.perf_counter()
    dijkstra_nodes, solved_dijkstra_grid, dijkstra_steps = dijkstra(dijkstra_grid)
    dijkstra_end = time.perf_counter()

    astar_start = time.perf_counter()
    astar_nodes, solved_astar_grid, astar_steps = astar(astar_grid)
    astar_end = time.perf_counter()

    return {
        "generated_grid": generated_grid.to_list(),
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "bfs_steps": bfs_steps, "time_ms": (bfs_end - bfs_start) * 1000},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "dfs_steps": dfs_steps, "time_ms": (dfs_end - dfs_start) * 1000},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "dijkstra_steps": dijkstra_steps, "time_ms": (dijkstra_end - dijkstra_start) * 1000},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "astar_steps": astar_steps, "time_ms": (astar_end - astar_start) * 1000},
    }

@app.post("/solve_grid")
def solve_grid(request: GridRequest):
    bfs_grid = Grid(request.grid)
    dfs_grid = Grid(request.grid)
    dijkstra_grid = Grid(request.grid)
    astar_grid = Grid(request.grid)
    

    bfs_nodes, solved_bfs_grid, bfs_steps = bfs(bfs_grid)
    dfs_nodes, solved_dfs_grid, dfs_steps = dfs(dfs_grid)
    dijkstra_nodes, solved_dijkstra_grid, dijkstra_steps = dijkstra(dijkstra_grid)
    astar_nodes, solved_astar_grid, astar_steps = astar(astar_grid)

    return {
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "bfs_steps": bfs_steps},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "dfs_steps": dfs_steps},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "dijkstra_steps": dijkstra_steps},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "astar_steps": astar_steps},
    }

@app.post("/solve_board")
def solve_board(request: SudokuRequest):

    board = Board(request.board)
    board.append_positions()
    
    solved, steps = solver(board)

    if not solved:
        return {
            "solved": solved,
            "board_steps": steps,
            "board": board.to_list(),
            "error": "Board is unsolvable"
        }

    return {
        "solved": solved,
        "board_steps": steps,
        "board": board.to_list()
    }