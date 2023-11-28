# src\repository\contacts.py
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, extract

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from src.services.auth import Auth

from datetime import datetime, timedelta

from fastapi import HTTPException, status

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()




async def search_contacts(
    user: User,
    db: Session,
    search_key: Optional[str] = None,
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None
) -> List[Contact]:
    filters = {
        "name": name,
        "lastname": lastname,
        "email": email,
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    contacts = db.query(Contact).filter(Contact.id == user.id).filter(
        or_(
            Contact.name == search_key,
            Contact.lastname == search_key,
            Contact.email == search_key,
            **filters
        )).all()

    if email:
        contacts += db.query(Contact).filter(Contact.id == user.id).filter(Contact.email == email).all()
    return contacts



async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.user_id == user.id, Contact.id == contact_id).first()



async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(name=body.name, 
                      lastname=body.lastname, 
                      email=body.email, 
                      phone=body.phone, 
                      birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


# щось не працює при оптимізації запиту для цього скрипта. Залишаємо поки попередній варіант

# async def create_contact(body: ContactModel, user: User, auth: Auth, db: Session) -> Contact:
#     hashed_password = auth.get_password_hash(body.password)

#     if user.id != body.user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    
#     contact = Contact(name=body.name, 
#                       lastname=body.lastname, 
#                       email=body.email, 
#                       phone=body.phone, 
#                       birthday=body.birthday,
#                       password=hashed_password, # Передаємо хешований пароль
#                       user_id=user.id)
#     db.add(contact)
#     db.commit()
#     db.refresh(contact) # щоб з'явився id
#     # db.flush() # не фіксує транзакцію. потрібно викликати commit відразу після flush
#     return contact

# def is_contact_owner(contact: Contact, user: User) -> bool:
#     return contact.user_id == user.id


# async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
#     contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    
#     if contact and is_contact_owner(contact, user):
#         db.delete(contact)
#         db.commit()
#         return contact
#     else:
#         return None



async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(
            Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact



async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == user.id).filter(and_(Contact.id == contact_id)).first()
    
    if contact:
        # update only transmitted values
        for field, value in body.dict(exclude_unset=True).items():
            setattr(contact, field, value)
        
        db.commit()
    
    return contact



# async def get_week_birthdays(user: User, db: Session) -> List[Contact]:
#     contacts = db.query(Contact).filter(Contact.id == user.id).all()

#     matching_contacts = []
#     for contact in contacts:    
#         bd = datetime(year=datetime.now().year, 
#                       month=contact.birthday.month, 
#                       day=contact.birthday.day)

#         delta = bd - datetime.now()
#         week_delta = timedelta(days=7)

#         if timedelta(days=0) <= delta <= week_delta:
#             matching_contacts.append(contact)

#     return matching_contacts


# оптимізація запиту
async def get_week_birthdays(user: User, db: Session) -> List[Contact]:
    # Обчислюємо початок та кінець тижня
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Використовуємо SQL-запит для отримання контактів з народженнями в цей тиждень
    query = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            extract('month', Contact.birthday) == today.month,
            extract('day', Contact.birthday) >= start_of_week.day,
            extract('day', Contact.birthday) <= end_of_week.day
        )
    )

    matching_contacts = query.all()

    return matching_contacts
