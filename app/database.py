from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# Database URL (using SQLite in this example)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

# Set up SQLAlchemy engine and session maker
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()  # Rollback if there's an error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Base class for model definitions
Base = declarative_base()
