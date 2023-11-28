import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from src.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)

URI = settings.sqlalchemy_database_url
SQLALCHEMY_DATABASE_URL = URI

assert SQLALCHEMY_DATABASE_URL is not None, "SQLALCHEMY_DATABASE_URL UNDEFINED"

# Log the connection parameters
logging.info(f"Connecting to database with URI: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_db_connection():
    try:
        with engine.connect() as connection:
            # Execute a simple query to check the connection
            result = connection.execute(text("SELECT 1"))
            # Fetch the result
            _ = result.fetchone()
    except SQLAlchemyError as err:
        # Log the error
        logging.error(f"SQLAlchemyError: {err}")
        return False
    return True

# Check the connection
if check_db_connection():
    logging.info("Database connection successful")
else:
    logging.error("Database connection failed")
