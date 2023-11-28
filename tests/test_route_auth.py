import os
import sys
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from unittest.mock import MagicMock
import pytest

from src.repository import users as repository_users


# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.anyio
async def test_signup_user(client, user, monkeypatch):
    # Створюємо імітований об'єкт send_email_for_verification
    mock_send_email = MagicMock()
    
    # Заміщуємо функцію send_email_for_verification імітованим об'єктом
    monkeypatch.setattr("src.routes.auth.send_email_for_verification", mock_send_email)
    
    try:
        response = await client.post(
            "/api/auth/signup",
            json=user,
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["user"]["username"] == user.get("username")
        assert data["user"]["email"] == user.get("email")
        assert "id" in data["user"]
        
        # Перевіряємо, чи була викликана функція send_email_for_verification
        mock_send_email.assert_called_once_with(user.get("email"))
        
        logger.info("Test 'test_signup_user' passed successfully.")
    except Exception as e:
        logger.error(f"Test 'test_signup_user' failed with error: {e}")
        raise


@pytest.mark.anyio
async def test_repeat_signup_user(client, user):
    try:
        response = await client.post(
            "/api/auth/signup",
            json=user,
        )
        assert response.status_code == 409, response.text
        data = response.json()
        assert data["detail"] == "The account already exists"
        logger.info("Test 'test_repeat_signup_user' passed successfully.")
    except Exception as e:
        logger.error(f"Test 'test_repeat_signup_user' failed with error: {e}")
        raise


@pytest.mark.anyio
async def test_login_user_not_confirmed(client, user):
    try:
        response = await client.post(
            "/api/auth/login",
            data={"username": user.get("email"), "password": user.get("password")},
        )
        assert response.status_code == 401, response.text
        data = response.json()
        assert data["detail"] == "The email is not confirmed"
        logger.info("Test 'test_login_user_not_confirmed' passed successfully.")
    except Exception as e:
        logger.error(f"Test 'test_login_user_not_confirmed' failed with error: {e}")
        raise


@pytest.mark.anyio
async def test_login_user(client, session, user):
    current_user = await repository_users.get_user_by_email(user.get("email"), session)
    current_user.is_email_confirmed = True
    await session.commit()

    try:
        response = await client.post(
            "/api/auth/login",
            data={"username": user.get("email"), "password": user.get("password")},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["token_type"] == "bearer"
        logger.info("Test 'test_login_user' passed successfully.")
    except Exception as e:
        logger.error(f"Test 'test_login_user' failed with error: {e}")
        raise


@pytest.mark.anyio
async def test_login_wrong_email(client, user):
    try:
        response = await client.post(
            "/api/auth/login",
            data={"username": "email", "password": user.get("password")},
        )
        assert response.status_code == 401, response.text
        data = response.json()
        assert data["detail"] == "Invalid email"
        logger.info("Test 'test_login_wrong_email' passed successfully.")
    except Exception as e:
        logger.error(f"Test 'test_login_wrong_email' failed with error: {e}")
        raise


@pytest.mark.anyio
async def test_login_wrong_password(client, user):
    try:
        response = await client.post(
            "/api/auth/login",
            data={"username": user.get("email"), "password": "password"},
        )
        assert response.status_code == 401, response.text
        data = response.json()
        assert data["detail"] == "Invalid password"
        logger.info("Test 'test_login_wrong_password' passed successfully.")
    except Exception as e:
        logger.error(f"Test 'test_login_wrong_password' failed with error: {e}")
        raise
