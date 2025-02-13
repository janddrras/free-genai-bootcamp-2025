import os
import subprocess
from app.db.models import Base
from app.db.session import engine
from app.initial_data import init_db
from app.db.session import SessionLocal

def init() -> None:
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize sample data
    db = SessionLocal()
    init_db(db)

if __name__ == "__main__":
    init()
    print("Database initialized successfully!") 