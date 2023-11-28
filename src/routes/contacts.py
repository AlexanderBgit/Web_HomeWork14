# src\routes\contacts.py

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from fastapi_limiter.depends import RateLimiter #speed limit request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from src.database.conn_db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactUpdate, ContactResponse

from src.repository import contacts as repository_contacts
# from src.repository.contacts import repository_contacts

from src.services.auth import auth_service



router = APIRouter(prefix='/contacts')

# за замовчуванням
# @router.get("/", response_model=List[ContactResponse], name='return contacts1')
# async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     contacts = await repository_contacts.get_contacts(skip, limit, db)
#     return contacts

@router.get("/", response_model=List[ContactResponse], name='return contacts2',
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],)
async def read_contacts(contact_id: int | None = None, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.
    If contact_id is specified, it will return only the contact with that id.
    
    
    :param contact_id: int | None: Determine if the function is being called to get a single contact or all contacts
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    if contact_id is not None:
        contact = await repository_contacts.get_contact(contact_id, current_user, db)
        if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
        return [contact]
    else:
        contacts = await repository_contacts.get_contacts(0, 100, db)
        return contacts

# +
# @router.get("/{contact_id}", response_model=ContactResponse)
# async def read_contact(contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_contacts.get_contact(contact_id, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     return contact

@router.get("/{contact_id}", response_model=List[ContactResponse], name='get id')
async def read_contacts(limit: int = Query(10, le=1000), offset: int = 0, contact_id: int | None = None, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    if contact_id is not None:
        contact = await repository_contacts.get_contact(contact_id, current_user, db)
        if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
        return [contact]
    else:
        contacts = await repository_contacts.get_contacts(limit, offset, 0, 100, db)
        return contacts

# +
@router.put("/{contact_id}", response_model=ContactResponse, name='update contacts')
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact

# +
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes in a ContactModel object and returns the newly created contact.
    
    :param body: ContactModel: Pass the contact information to be created
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id from the token
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)

# +
@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# +
@router.get("/search/", response_model=List[ContactResponse], name='search by params')
async def search_contacts(
    search_key: Optional[str] = None,
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    The search_contacts function searches for contacts in the database.
        It can search by name, lastname, email or any combination of these fields.
        The function returns a list of contacts that match the search criteria.
    
    :param search_key: Optional[str]: Search for a contact by any of the fields in the database
    :param name: Optional[str]: Search for a contact by name
    :param lastname: Optional[str]: Search by lastname, but the function is not used anywhere in the code
    :param email: Optional[str]: Search for contacts by email
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is currently logged in
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(
        user=current_user,
        search_key=search_key,
        name=name,
        lastname=lastname,
        email=email,
        db=db
    )
    return contacts

# +
@router.get("/week_birthdays/", response_model=List[ContactResponse], name='birthdays')
async def get_week_birthdays(db: Session = Depends(get_db), 
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_week_birthdays function returns a list of contacts with birthdays in the next 7 days.
        The function takes two parameters: db and current_user. 
        The db parameter is used to connect to the database, while current_user is used for authentication purposes.
    
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user_id from the database
    :return: A list of contacts that have a birthday in the current week
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_week_birthdays(current_user, db)
    return contacts