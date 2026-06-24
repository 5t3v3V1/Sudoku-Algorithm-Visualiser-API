from database import engine
from models import Results

Results.metadata.create_all(bind = engine)