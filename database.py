from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import sessionmaker
import os

dotenv_path = find_dotenv()
# print(f"Loading .env from: {dotenv_path}")  # Debugging step
load_dotenv(dotenv_path, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")  # Debugging step
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
