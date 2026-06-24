from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime, UTC

Base = declarative_base()

class Results(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    algorithm = Column(String)
    nodes_visited = Column(Integer)
    solve_time = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

class BoardResults(Base):
    __tablename__ = "board results"

    id = Column(Integer, primary_key = True)
    moves = Column(Integer)
    solve_time = Column(Float)
    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(UTC))