from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime, UTC
from database import Base
from sqlalchemy import ForeignKey

class ResultAlgorithms(Base):
    __tablename__ = "result_algorithms"

    id = Column(Integer, primary_key = True)
    result_id = Column(Integer, ForeignKey("results.id"))
    algorithm = Column(String)
    nodes_visited = Column(Integer)
    solve_time = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

class Results(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key = True)
    best_algorithm = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

class BoardResults(Base):
    __tablename__ = "board_results"

    id = Column(Integer, primary_key = True)
    moves = Column(Integer)
    solve_time = Column(Float)
    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(UTC))