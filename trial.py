from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NameRequest(BaseModel):
    name: str

@app.post("/greet")
def greet(data: NameRequest):
    return {
        "message": f"Hello {data.name}"
    }


@app.get("/")
def home():
    return {
        "message": "Sudoku API is running"
    }

@app.get("/solver")
def hello():
    return {
        "message": "Hello World!"
    }