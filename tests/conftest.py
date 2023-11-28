
import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

from src.database.models import Base
from src.database.conn_db import get_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest
from fastapi.testclient import TestClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фікстура для налаштування бази даних для кожного модульного тесту
@pytest.fixture(scope="module")
def session():
    
    # Скидання та створення бази даних перед початком тестів
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Фікстура для створення тестового клієнта для FastAPI
@pytest.fixture(scope="module")
def client(session):
   

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

# Фікстура для тестового користувача
@pytest.fixture(scope="module")
def user():
    return {"username": "deadpool",
             "email": "deadpool@example.com",
              "password": "123456789", "id": 1}

# Тест реєстрації нового користувача
def test_register_user(client, user):
    logger.info("Running test_register_user")
    
    response = client.post("/register", json=user)
    
    assert response.status_code == 200
    assert response.json()["username"] == user["username"]
    
    logger.info("Test test_register_user passed")


# Тест отримання інформації про зареєстрованого користувача
def test_get_user(client, user):
    logger.info("Running test_get_user")

    # Реєструємо нового користувача
    response_register = client.post("/register", json=user)
    assert response_register.status_code == 200
    
    # Отримуємо інформацію про користувача
    response_get_user = client.get(f"/user/{user['id']}")
    assert response_get_user.status_code == 200
    assert response_get_user.json()["username"] == user["username"]
    
    logger.info("Test test_get_user passed")


# Тест оновлення інформації про користувача
def test_update_user(client, user):
    logger.info("Running test_update_user")