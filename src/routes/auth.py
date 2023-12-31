from typing import List

from fastapi import (
    APIRouter, HTTPException, Depends, status, Security, 
    BackgroundTasks, Request
    )
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from sqlalchemy.orm import Session

from src.database.conn_db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.database.models import User
from src.services.email import send_email 


router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# створення нового користувача, якщо такого email не існує
@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserModel, 
                 background_tasks: BackgroundTasks, request: Request,
                 db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It also sends an email to the user with a link to confirm their account.
        The function returns a JSON object containing the newly created user and 
        details about what happened.
    
    :param body: UserModel: Get the user data from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background
    :param request: Request: Get the base url of the application
    :param db: Session: Access the database
    :return: A dictionary with the user and a detail message
    :doc-author: Trelent
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created"}




# витягує користувача з бази даних з його email
@router.post("/login", response_model=TokenModel)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    The login function is used to authenticate a user.
    It takes the email and password of the user as input, and returns an access token if authentication was successful.
    The access token can be used in subsequent requests to identify the authenticated user.
    
    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Get a database session
    :return: The access_token and refresh_token
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.username, db)
    # user = db.query(User).filter(User.email == body.username).first() # username = email
# робочий варіант    
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
    #     )
    # if not user.confirmed:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
    #     )
    # if not auth_service.verify_password(body.password, user.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
    #     )
    # # Generate JWT
    # access_token = await auth_service.create_access_token(data={"sub": user.email})
    # refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    # await repository_users.update_token(user, refresh_token, db)
    # return {
    #     "access_token": access_token,
    #     "refresh_token": refresh_token,
    #     "token_type": "bearer",
    # }

# test branch - no email notification in the database
    if user:
        if not user.confirmed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
        )
        if not auth_service.verify_password(body.password, user.password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# декодує токен оновлення refresh_token та витягує відповідного користувача з бази даних
# потім створює/оновлює нові токени
@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access_token, 
        a new refresh_token, and the type of token (bearer).
    
    :param credentials: HTTPAuthorizationCredentials: Get the token from the request headers
    :param db: Session: Get the database session
    :param : Get the user's email from the token
    :return: An object with the following properties:
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# @router.get("/")
# async def root():
#     return {"message": "Hello REST API Authorization"}


@router.get("/secret")
async def read_item(current_users: User = Depends(auth_service.get_current_user)):
    return{"message":'secret router', "contact": current_users.email}


# + hw13
@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        Then, it checks if that user exists in our database, and if they do not exist, 
        an HTTP 400 error is raised. If they do exist but their account has already been confirmed,
        then a message saying so will be returned. Otherwise (if they are found in our database 
        and their account has not yet been confirmed), we call repository_users' confirmed_email function 
        with that email as its
    
    :param token: str: Get the token from the url
    :param db: Session: Access the database
    :return: A dict with the message
    :doc-author: Trelent
    """

    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

# + hw13
@router.post('/request_email')
async def request_email(body: RequestEmail, 
                        background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}