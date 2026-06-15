from fastapi import FastAPI
from pydantic import BaseModel
from solver import solver
import random
from validator import is_valid
from classes import Grid, SudokuRequest
from generator import board_generator
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


app = FastAPI()

@app.get("/generate")
def generate_board():
    board = [[], [], [], [], [], [], [], [], []]
    for y in range(9):
        for x in range(9):
            board[y].append(0)

    board = Grid(board)
    board.append_positions()

    board_generator(board)

    positions = list(board.nodes.keys())

    random.shuffle(positions)

    for position in positions[:40]:
        board.nodes[position].number = 0

    return {
        "board": board.to_list()
    }

@app.post("/solve")
def solve_board(request: SudokuRequest):

    grid = Grid(request.board)
    grid.append_positions()
    
    solved = solver(grid)

    if not solved:
        return {
            "solved": solved,
            "board": grid.to_list(),
            "error": "Board is unsolvable"
        }

    return {
        "solved": solved,
        "board": grid.to_list()
    }