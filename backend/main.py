from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from live_solver import livesolver
from solver import solver
import random
import copy
import time
from classes import Board, SudokuRequest, Grid, Grid_Node, GridRequest
from generator import board_generator, grid_generator
from pathfinding_algorithms import bfs, dfs, dijkstra, astar
from live_pathfinding_algorithms import livebfs, livedfs, livedijkstra, liveastar
from fastapi.middleware.cors import CORSMiddleware
from models import Results, BoardResults, ResultAlgorithms
from database import SessionLocal
from concurrent.futures import ThreadPoolExecutor
import asyncio
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

@app.websocket("/counter")
async def counter(websocket: WebSocket):
    await websocket.accept()

    for number in range(10):
        await websocket.send_json(number)
        await asyncio.sleep(1)

@app.websocket("/generate_solve_board")
async def generate_solve_board(websocket: WebSocket):
    await websocket.accept()
    db = SessionLocal()
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
    
    solved, board_moves = livesolver(board, websocket)

    end = time.perf_counter()

    board_result = BoardResults(
        moves = board_moves,
        solve_time = (end - start) * 1000
    )

    db.add(board_result)
    db.commit()
    db.close()

    if not solved:
        await websocket.send_json({
            "type": "unfinished",
            "solved": solved,
            "generated_board": generated_board.to_list(),
            "solved_board": board.to_list(),
            "moves": board_moves,
            "time_ms": (end - start) * 1000
        })
    
        await websocket.close()

    await websocket.send_json({
        "type": "finished",
        "solved": solved,
        "generated_board": generated_board.to_list(),
        "solved_board": board.to_list(),
        "moves": board_moves,
        "time_ms": (end - start) * 1000
    })
    
    await websocket.close()

@app.websocket("/generate_solve_grid")
async def generate_solve_grid(websocket: WebSocket):
    websocket.accept()
    db = SessionLocal()
    grid = grid_generator()
    generated_grid = grid.copy()
    generated_grid = Grid(generated_grid)
    generated_grid.append_nodes()

    bfs_grid = Grid(grid)
    dfs_grid = Grid(grid)
    dijkstra_grid = Grid(grid)
    astar_grid = Grid(grid)
    
    with ThreadPoolExecutor as executor:
        bfs_future = executor.submit(livebfs, (bfs_grid, websocket))
        dfs_future = executor.submit(livedfs, (dfs_grid, websocket))
        dijkstra_future = executor.submit(livedijkstra, (dijkstra_grid, websocket))
        astar_future = executor.submit(liveastar, (astar_grid, websocket))

        bfs_nodes, solved_bfs_grid, bfs_solve_time = bfs_future.result()
        dfs_nodes, solved_dfs_grid, dfs_solve_time = dfs_future.result()
        dijkstra_nodes, solved_dijkstra_grid, dijkstra_solve_time = dijkstra_future.result()
        astar_nodes, solved_astar_grid, astar_solve_time = astar_future.result()

    results = {
        "BFS": bfs_solve_time,
        "DFS": dfs_solve_time,
        "Dijkstra": dijkstra_solve_time,
        "A*": astar_solve_time
    }

    best_time = min(results, key=results.get)

    group_result = Results(
        best_algorithm = best_time
    )

    db.add(group_result)
    db.flush()

    bfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "BFS",
        nodes_visited = bfs_nodes,
        solve_time = bfs_solve_time
    )

    db.add(bfs_result)

    dfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "DFS",
        nodes_visited = dfs_nodes,
        solve_time = dfs_solve_time
    )

    db.add(dfs_result)

    dijkstra_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "Dijkstra",
        nodes_visited = dijkstra_nodes,
        solve_time = dijkstra_solve_time
    )

    db.add(dijkstra_result)

    astar_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "A*",
        nodes_visited = astar_nodes,
        solve_time = astar_solve_time
    )

    db.add(astar_result)

    db.commit()
    db.close()

    await websocket.send_json({
        "type": "finished",
        "generated_grid": generated_grid.to_list(),
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "time_ms": bfs_solve_time},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "time_ms": dfs_solve_time},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "time_ms": dijkstra_solve_time},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "time_ms": astar_solve_time},
    })
    
    await websocket.close()

@app.websocket("/solve_board")
async def solve_board(request: SudokuRequest, websocket: WebSocket):
    websocket.accept()
    db = SessionLocal()
    board = Board(request.board)
    board.append_positions()
    
    input_board = copy.deepcopy(board)

    start = time.perf_counter()
    
    solved, board_moves = livesolver(board, websocket)

    end = time.perf_counter()

    board_result = BoardResults(
        moves = board_moves,
        solve_time = (end - start) * 1000
    )

    db.add(board_result)
    db.commit()
    db.close()

    if not solved:
        await websocket.send_json({
            "type": "unfinished",
            "solved": solved,
            "generated_board": input_board.to_list(),
            "solved_board": board.to_list(),
            "moves": board_moves,
            "time_ms": (end - start) * 1000
        })
    
        await websocket.close()

    await websocket.send_json({
        "type": "finished",
        "solved": solved,
        "generated_board": input_board.to_list(),
        "solved_board": board.to_list(),
        "moves": board_moves,
        "time_ms": (end - start) * 1000
    })
    
    await websocket.close()

@app.websocket("/solve_grid")
async def solve_grid(request: SudokuRequest, websocket: WebSocket):
    websocket.accept()
    db = SessionLocal()
    input_grid = request.grid.copy()
    input_grid = Grid(input_grid)
    input_grid.append_nodes()

    bfs_grid = Grid(request.grid)
    dfs_grid = Grid(request.grid)
    dijkstra_grid = Grid(request.grid)
    astar_grid = Grid(request.grid)

    with ThreadPoolExecutor as executor:
        bfs_future = executor.submit(livebfs, bfs_grid)
        dfs_future = executor.submit(livedfs, dfs_grid)
        dijkstra_future = executor.submit(livedijkstra, dijkstra_grid)
        astar_future = executor.submit(liveastar, astar_grid)

        bfs_nodes, solved_bfs_grid, bfs_solve_time = bfs_future.result()
        dfs_nodes, solved_dfs_grid, dfs_solve_time = dfs_future.result()
        dijkstra_nodes, solved_dijkstra_grid, dijkstra_solve_time = dijkstra_future.result()
        astar_nodes, solved_astar_grid, astar_solve_time = astar_future.result()

    results = {
        "BFS": bfs_solve_time,
        "DFS": dfs_solve_time,
        "Dijkstra": dijkstra_solve_time,
        "A*": astar_solve_time
    }

    best_time = min(results, key=results.get)

    group_result = Results(
        best_algorithm = best_time
    )

    db.add(group_result)
    db.flush()

    bfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "BFS",
        nodes_visited = bfs_nodes,
        solve_time = bfs_solve_time
    )

    db.add(bfs_result)

    dfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "DFS",
        nodes_visited = dfs_nodes,
        solve_time = dfs_solve_time
    )

    db.add(dfs_result)

    dijkstra_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "Dijkstra",
        nodes_visited = dijkstra_nodes,
        solve_time = dijkstra_solve_time
    )

    db.add(dijkstra_result)

    astar_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "A*",
        nodes_visited = astar_nodes,
        solve_time = astar_solve_time
    )

    db.add(astar_result)

    db.commit()
    db.close()

    await websocket.send_json({
        "type": "finished",
        "generated_grid": input_grid.to_list(),
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "time_ms": bfs_solve_time},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "time_ms": dfs_solve_time},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "time_ms": dijkstra_solve_time},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "time_ms": astar_solve_time},
    })
    
    await websocket.close()

@app.get("/generate_solve_board_prews")
def generate_solve_board_prews():
    db = SessionLocal()
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
    
    solved, board_steps, board_moves = solver(board)

    end = time.perf_counter()

    board_result = BoardResults(
        moves = board_moves,
        solve_time = (end - start) * 1000
    )

    db.add(board_result)
    db.commit()
    db.close()

    if not solved:
        return {
            "solved": solved,
            "generated_board": generated_board.to_list(),
            "board_steps": board_steps,
            "unsolved_board": board.to_list(),
            "error": "Board is unsolvable"
        }

    return {
        "solved": solved,
        "generated_board": generated_board.to_list(),
        "board_steps": board_steps,
        "solved_board": board.to_list(),
        "moves": board_moves,
        "time_ms": (end - start) * 1000
    }

@app.get("/generate_solve_grid_prews")
def generate_solve_grid_prews():
    db = SessionLocal()
    grid = grid_generator()
    generated_grid = grid.copy()
    generated_grid = Grid(generated_grid)
    generated_grid.append_nodes()

    bfs_grid = Grid(grid)
    dfs_grid = Grid(grid)
    dijkstra_grid = Grid(grid)
    astar_grid = Grid(grid)
    
    with ThreadPoolExecutor as executor:
        bfs_future = executor.submit(bfs, bfs_grid)
        dfs_future = executor.submit(dfs, dfs_grid)
        dijkstra_future = executor.submit(dijkstra, dijkstra_grid)
        astar_future = executor.submit(astar, astar_grid)

        bfs_nodes, solved_bfs_grid, bfs_steps, bfs_solve_time = bfs_future.result()
        dfs_nodes, solved_dfs_grid, dfs_steps, dfs_solve_time = dfs_future.result()
        dijkstra_nodes, solved_dijkstra_grid, dijkstra_steps, dijkstra_solve_time = dijkstra_future.result()
        astar_nodes, solved_astar_grid, astar_steps, astar_solve_time = astar_future.result()

    results = {
        "BFS": bfs_solve_time,
        "DFS": dfs_solve_time,
        "Dijkstra": dijkstra_solve_time,
        "A*": astar_solve_time
    }

    best_time = min(results, key=results.get)

    group_result = Results(
        best_algorithm = best_time
    )

    db.add(group_result)
    db.flush()

    bfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "BFS",
        nodes_visited = bfs_nodes,
        solve_time = bfs_solve_time
    )

    db.add(bfs_result)

    dfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "DFS",
        nodes_visited = dfs_nodes,
        solve_time = dfs_solve_time
    )

    db.add(dfs_result)

    dijkstra_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "Dijkstra",
        nodes_visited = dijkstra_nodes,
        solve_time = dijkstra_solve_time
    )

    db.add(dijkstra_result)

    astar_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "A*",
        nodes_visited = astar_nodes,
        solve_time = astar_solve_time
    )

    db.add(astar_result)

    db.commit()
    db.close()

    return {
        "generated_grid": generated_grid.to_list(),
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "bfs_steps": bfs_steps, "time_ms": bfs_solve_time},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "dfs_steps": dfs_steps, "time_ms": dfs_solve_time},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "dijkstra_steps": dijkstra_steps, "time_ms": dijkstra_solve_time},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "astar_steps": astar_steps, "time_ms": astar_solve_time},
    }

@app.post("/solve_grid_prews")
def solve_grid_prews(request: GridRequest):
    db = SessionLocal()
    input_grid = request.grid.copy()
    input_grid = Grid(input_grid)
    input_grid.append_nodes()

    bfs_grid = Grid(request.grid)
    dfs_grid = Grid(request.grid)
    dijkstra_grid = Grid(request.grid)
    astar_grid = Grid(request.grid)

    with ThreadPoolExecutor as executor:
        bfs_future = executor.submit(bfs, bfs_grid)
        dfs_future = executor.submit(dfs, dfs_grid)
        dijkstra_future = executor.submit(dijkstra, dijkstra_grid)
        astar_future = executor.submit(astar, astar_grid)

        bfs_nodes, solved_bfs_grid, bfs_steps, bfs_solve_time = bfs_future.result()
        dfs_nodes, solved_dfs_grid, dfs_steps, dfs_solve_time = dfs_future.result()
        dijkstra_nodes, solved_dijkstra_grid, dijkstra_steps, dijkstra_solve_time = dijkstra_future.result()
        astar_nodes, solved_astar_grid, astar_steps, astar_solve_time = astar_future.result()

    results = {
        "BFS": bfs_solve_time,
        "DFS": dfs_solve_time,
        "Dijkstra": dijkstra_solve_time,
        "A*": astar_solve_time
    }

    best_time = min(results, key=results.get)

    group_result = Results(
        best_algorithm = best_time
    )

    db.add(group_result)
    db.flush()

    bfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "BFS",
        nodes_visited = bfs_nodes,
        solve_time = bfs_solve_time
    )

    db.add(bfs_result)

    dfs_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "DFS",
        nodes_visited = dfs_nodes,
        solve_time = dfs_solve_time
    )

    db.add(dfs_result)

    dijkstra_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "Dijkstra",
        nodes_visited = dijkstra_nodes,
        solve_time = dijkstra_solve_time
    )

    db.add(dijkstra_result)

    astar_result = ResultAlgorithms(
        result_id = group_result.id,
        algorithm = "A*",
        nodes_visited = astar_nodes,
        solve_time = astar_solve_time
    )

    db.add(astar_result)

    db.commit()
    db.close()

    return {
        "generated_grid": input_grid.to_list(),
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "bfs_steps": bfs_steps, "time_ms": bfs_solve_time},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "dfs_steps": dfs_steps, "time_ms": dfs_solve_time},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "dijkstra_steps": dijkstra_steps, "time_ms": dijkstra_solve_time},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "astar_steps": astar_steps, "time_ms": astar_solve_time},
    }

@app.post("/solve_board_prews")
def solve_board_prews(request: SudokuRequest):
    db = SessionLocal()
    board = Board(request.board)
    board.append_positions()
    
    input_board = copy.deepcopy(board)

    start = time.perf_counter()
    
    solved, board_steps, board_moves = solver(board)

    end = time.perf_counter()

    board_result = BoardResults(
        moves = board_moves,
        solve_time = (end - start) * 1000
    )

    db.add(board_result)
    db.commit()
    db.close()

    if not solved:
        return {
            "solved": solved,
            "generated_board": input_board.to_list(),
            "board_steps": board_steps,
            "unsolved_board": board.to_list(),
            "error": "Board is unsolvable"
        }

    return {
        "solved": solved,
        "generated_board": input_board.to_list(),
        "board_steps": board_steps,
        "solved_board": board.to_list(),
        "moves": board_moves,
        "time_ms": (end - start) * 1000
    }