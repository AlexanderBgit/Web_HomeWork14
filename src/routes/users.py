# src\routes\users.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session


from src.database.conn_db import get_db
from src.database.models import User

# from src.services.auth import get_current_user
# import cloudinary
# from cloudinary.uploader import upload

from src.schemas import  UserResponse, UserDb
from src.services.cloudinary import Cloudinary

# from src.config import settings

from src.services.auth import auth_service
router = APIRouter(prefix="/users", tags=["users"])




# @router.get("/me/", response_model=UserResponse, response_model_exclude_none=True)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

@router.get("/me", response_model=UserDb)
async def read_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_me function returns the current user's information.
        ---
        get:
          tags: [user]
          description: Returns the current user's information. 
          responses:
            200:  # HTTP status code 200 means &quot;OK&quot;
              description: The requested resource was returned successfully.
    
    :param current_user: User: Get the current user from the database
    :return: The current user
    :doc-author: Trelent
    """
    user_db = UserDb(**current_user.__dict__.copy())
    return user_db



@router.patch("/avatar", response_model=UserResponse, 
              response_model_exclude_unset=True)
async def update_avatar_user(
    file: UploadFile = File(), 
    current_user: User = Depends(auth_service.get_current_user), 
    db: Session = Depends(get_db)
):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The file to be uploaded.
            current_user (User): The currently logged in user.  This is passed by the auth_service dependency, which uses JWT tokens to authenticate users and pass them into functions as dependencies when they are logged in.  If no token is present, this will return None and raise an HTTPException with status code 401 UNAUTHORIZED, which means &quot;you must log in first&quot;.  
            db (Session): A database Session instance provided by SQLAlchemy's sc
    
    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user information
    :param db: Session: Access the database
    :return: A userresponse object
    :doc-author: Trelent
    """
    public_id = Cloudinary.generate_public_id_by_email(str(current_user.email))
    r = Cloudinary.upload(file.file, public_id)

    src_url = Cloudinary.generate_url(r, public_id)
    user_db = UserDb(**current_user.__dict__.copy())
    user = await auth_service.update_avatar(current_user.email, src_url, db)
    return UserResponse(user=user_db)