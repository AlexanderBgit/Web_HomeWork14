# src\services\auth.py
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.conn_db import get_db
from src.repository import users as repository_users
from src.database.models import User
from src.schemas import UserResponse, UserDb


import logging
logger = logging.getLogger(__name__)

AUTH_LOGIN_URL = "/api/auth/login"

class Auth:
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # SECRET_KEY = "secret_key"
    # ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=AUTH_LOGIN_URL)


# з цією конструкцією не стартує для рядків, якщо oauth2_scheme не винесена за межі def __init__
# from src.repository import contacts as repository_contacts
# from src.repository import users as repository_users

    def __init__(self, schemes: list, deprecated: str, 
                 secret_key: str, algorithm: str, token_url: str = AUTH_LOGIN_URL):
        self.pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url, auto_error=False)
        # self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # генерація хешованого паролю
    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)



    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            # чим довше існує access_token, тим більше часу має зловмисник у разі злому аккаунта
            expire = datetime.utcnow() + timedelta(weeks=2) 
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')


    # async def get_current_user(self, token: str = Depends(lambda: self.oauth2_scheme), db: Session = Depends(get_db)):
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            logger.error(f"JWT Error: {e}, Token: {token}")
            raise credentials_exception
        
        logger.info(f"Decoded Token: {token}, Payload: {payload}, Email: {email}")

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token
    
    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


    async def update_avatar(self, email: str, url: str, db: Session) -> UserDb:
        user = await repository_users.update_avatar(email, url, db)
        return user




# auth_service = Auth()
auth_service = Auth(
    schemes=["bcrypt"],
    deprecated="auto",
    secret_key="secret_key",
    algorithm="HS256",
    # token_url=AUTH_LOGIN_URL
)

