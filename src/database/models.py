from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    DateTime, 
    func, 
    event, 
    Date
    )
from sqlalchemy.orm import relationship, declarative_base

# from src.schemas import UserResponse, UserDb

Base = declarative_base()


class Contact(Base):
    # mandatory data
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, default="None", nullable=False)
    birthday = Column(Date, default=None, nullable=True)
    
    # optional data
    age = Column(Integer)
    additional = Column(String, default="None", nullable=False)
    description = Column(String, default="None", index=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship("User", backref="contacts")
    created_at = Column(DateTime, default=func.now())  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('iat', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) 
                for column in self.__table__.columns if hasattr(self, column.name)}
    
    # def as_db(self) -> UserDb:
    #     return UserDb(
    #         id=self.id,
    #         username=self.username,
    #         email=self.email,
    #         created_at=self.created_at,
    #         avatar=self.avatar,
    #         confirmed=self.confirmed
    #     )

    # def as_response(self) -> UserResponse:
    #     return UserResponse(
    #         user=self.as_db(),  # або dict(self.as_db())
    #         detail="User successfully created"
    #     ).dict()