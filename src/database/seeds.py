from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import date

from models import Base, Contact
from conn_db import ALCHEMY_DB_URL


engine = create_engine(ALCHEMY_DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(bind=engine)

fake = Faker('uk_UA')

# Create contacts
for _ in range(10):
    contact = Contact(
        name=fake.name(),
        lastname=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number(),
        birthday=fake.date_of_birth(minimum_age=18, maximum_age=65),
        additional=fake.text(max_nb_chars=10),
        description = fake.text(max_nb_chars=20)  
    )

    session.add(contact)

session.commit()

