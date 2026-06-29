from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from live_solver import livesolver
from solver import solver
import random
import copy
import time
from classes import Board, DifficultyRequest, Grid, Grid_Node, GridRequest
from generator import board_generator, grid_generator
from pathfinding_algorithms import bfs, dfs, dijkstra, astar
from live_pathfinding_algorithms import livebfs, livedfs, livedijkstra, liveastar
from fastapi.middleware.cors import CORSMiddleware
from models import Results, BoardResults, ResultAlgorithms
from database import SessionLocal
from concurrent.futures import ThreadPoolExecutor
import asyncio
from sqlalchemy import func
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://algorithm-visualiser-api.vercel.app"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def grid_db_helper(db, results_dict):
    best_time = min(results_dict, key=lambda k: results_dict[k][1])

    group_result = Results(best_algorithm = best_time)
    db.add(group_result)
    db.flush()

    for algorithm, (nodes, time_ms) in results_dict.items():
        db.add(ResultAlgorithms(
            result_id = group_result.id,
            algorithm = algorithm,
            nodes_visited = nodes,
            solve_time = time_ms
        ))

    db.commit()
    db.close()

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

@app.get("/stats")
def stats():
    db = SessionLocal()
    best_counts = db.query(Results.best_algorithm, func.count(Results.best_algorithm)).group_by(Results.best_algorithm).all()
    avg_time = db.query(ResultAlgorithms.algorithm, func.avg(ResultAlgorithms.solve_time)).group_by(ResultAlgorithms.algorithm).all()
    boards_solved = db.query(func.count(BoardResults.id)).scalar()
    grids_solved = db.query(func.count(Results.id)).scalar()
    db.close()

    best_dict = {row[0]: row[1] for row in best_counts}
    avg_dict = {row[0]: row[1] for row in avg_time}
    return {
        "bfs": {"best": best_dict.get("BFS", 0), "avg": avg_dict.get("BFS", 0)},
        "dfs": {"best": best_dict.get("DFS", 0), "avg": avg_dict.get("DFS", 0)},
        "dijkstra": {"best": best_dict.get("Dijkstra", 0), "avg": avg_dict.get("Dijkstra", 0)},
        "astar": {"best": best_dict.get("A*", 0), "avg": avg_dict.get("A*", 0)},
        "boards_solved": boards_solved,
        "grids_solved": grids_solved
    }

@app.websocket("/generate_solve_board")
async def generate_solve_board(websocket: WebSocket):
    await websocket.accept()
    db = SessionLocal()
    data = await websocket.receive_json()
    difficulty = data["difficulty"]
    board = [[], [], [], [], [], [], [], [], []]
    for y in range(9):
        for x in range(9):
            board[y].append(0)

    board = Board(board)
    board.append_positions()

    board_generator(board)

    positions = list(board.nodes.keys())

    random.shuffle(positions)

    for position in positions[:difficulty]:
        board.nodes[position].number = 0

    generated_board = copy.deepcopy(board)

    start = time.perf_counter()
    
    solved, board_moves = await livesolver(board, websocket)

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
            "type": "unfinished_board",
            "generated_board": generated_board.to_list(),
            "solved_board": board.to_list(),
            "moves": board_moves,
            "time_ms": (end - start) * 1000
        })
    
        await websocket.close()

    await websocket.send_json({
        "type": "finished_board",
        "generated_board": generated_board.to_list(),
        "solved_board": board.to_list(),
        "moves": board_moves,
        "time_ms": (end - start) * 1000
    })
    
    await websocket.close()
    return

@app.websocket("/generate_solve_grid")
async def generate_solve_grid(websocket: WebSocket):
    await websocket.accept()
    db = SessionLocal()
    grid = grid_generator()
    generated_grid = grid.copy()
    generated_grid = Grid(generated_grid)
    generated_grid.append_nodes()

    bfs_grid = Grid(grid)
    dfs_grid = Grid(grid)
    dijkstra_grid = Grid(grid)
    astar_grid = Grid(grid)
    
    results = await asyncio.gather(
        livebfs(bfs_grid, websocket),
        livedfs(dfs_grid, websocket),
        livedijkstra(dijkstra_grid, websocket),
        liveastar(astar_grid, websocket),
    )

    bfs_nodes, solved_bfs_grid, bfs_solve_time = results[0]
    dfs_nodes, solved_dfs_grid, dfs_solve_time = results[1]
    dijkstra_nodes, solved_dijkstra_grid, dijkstra_solve_time = results[2]
    astar_nodes, solved_astar_grid, astar_solve_time = results[3]

    grid_db_helper(db, {
        "BFS": (bfs_nodes, bfs_solve_time),
        "DFS": (dfs_nodes, dfs_solve_time),
        "Dijkstra": (dijkstra_nodes, dijkstra_solve_time),
        "A*": (astar_nodes, astar_solve_time)
    })

    await websocket.send_json({
        "type": "finished",
        "generated_grid": generated_grid.to_list(),
        "bfs": {"algorithm": "BFS", "bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "time_ms": bfs_solve_time},
        "dfs": {"algorithm": "DFS", "dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "time_ms": dfs_solve_time},
        "dijkstra": {"algorithm": "Dijkstra", "dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "time_ms": dijkstra_solve_time},
        "astar": {"algorithm": "A*", "astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "time_ms": astar_solve_time},
    })
    
    await websocket.close()


@app.post("/generate_solve_board_prews")
def generate_solve_board_prews(difficulty: DifficultyRequest):
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

    for position in positions[:difficulty]:
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
    
    with ThreadPoolExecutor() as executor:
        bfs_future = executor.submit(bfs, bfs_grid)
        dfs_future = executor.submit(dfs, dfs_grid)
        dijkstra_future = executor.submit(dijkstra, dijkstra_grid)
        astar_future = executor.submit(astar, astar_grid)

        bfs_nodes, solved_bfs_grid, bfs_steps, bfs_solve_time = bfs_future.result()
        dfs_nodes, solved_dfs_grid, dfs_steps, dfs_solve_time = dfs_future.result()
        dijkstra_nodes, solved_dijkstra_grid, dijkstra_steps, dijkstra_solve_time = dijkstra_future.result()
        astar_nodes, solved_astar_grid, astar_steps, astar_solve_time = astar_future.result()

    grid_db_helper(db, {
        "BFS": (bfs_nodes, bfs_solve_time),
        "DFS": (dfs_nodes, dfs_solve_time),
        "Dijkstra": (dijkstra_nodes, dijkstra_solve_time),
        "A*": (astar_nodes, astar_solve_time)
    })

    return {
        "generated_grid": generated_grid.to_list(),
        "bfs": {"bfs_nodes": bfs_nodes, "solved_bfs_grid": solved_bfs_grid.to_list(), "bfs_steps": bfs_steps, "time_ms": bfs_solve_time},
        "dfs": {"dfs_nodes": dfs_nodes, "solved_dfs_grid": solved_dfs_grid.to_list(), "dfs_steps": dfs_steps, "time_ms": dfs_solve_time},
        "dijkstra": {"dijkstra_nodes": dijkstra_nodes, "solved_dijkstra_grid": solved_dijkstra_grid.to_list(), "dijkstra_steps": dijkstra_steps, "time_ms": dijkstra_solve_time},
        "astar": {"astar_nodes": astar_nodes, "solved_astar_grid": solved_astar_grid.to_list(), "astar_steps": astar_steps, "time_ms": astar_solve_time},
    }