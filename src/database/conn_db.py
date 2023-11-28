from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from src.config import settings
import logging


logging.basicConfig(level=logging.INFO)

URI = settings.sqlalchemy_database_url
SQLALCHEMY_DATABASE_URL = URI

assert SQLALCHEMY_DATABASE_URL is not None, "SQLALCHEMY_DATABASE_URL UNDEFINED"
logging.info(f"Connecting to database with URI: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #загальне по документації

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        print("SQLAlchemyError:", err)
        logging.error(f"SQLAlchemyError: {err}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()