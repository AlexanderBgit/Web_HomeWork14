import unittest
from unittest.mock import MagicMock, patch
import uuid

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.engine.result import ChunkedIteratorResult


import logging
from datetime import date
import sys
import os
logging.basicConfig(level=logging.INFO)

# Додаємо шлях до кореневого каталогу проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.environ.get('PYTHONPATH'))


from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    get_week_birthdays,
    search_contacts,
    )


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        # self.user = User(id=uuid.uuid4())
        self.user = User(id=1)

        self.body = ContactModel(
        name="Gupalo",
        lastname="Vasyl",
        email="gv@test.ua",
        phone="99558866",
        age=25,
        description="some place",)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_get_contact(self):
            contact_mock = Contact(
                id=1,
                name="John",
                lastname="Wick",
                email="john@example.com",
                phone="123456789",
            )
            with patch("src.repository.contacts.Session.query") as query_mock:
                query_mock.return_value.filter().first.return_value = contact_mock

                result = await get_contact(contact_id=1, user=self.user, db=self.session)

                self.assertEqual(result.id, 1)
                self.assertEqual(result.name, "John")



    async def test_get_contacts_not_found(self):
            with patch("src.repository.contacts.Session.query") as query_mock:
                query_mock.return_value.filter().offset().limit().return_value = []

                result = await get_contacts(
                    skip=0,
                    limit=10,
                    user=self.user,
                    db=self.session,
                )
                self.assertEqual(len(result), 0, f"Expected an empty list but got {result}")
                logging.info(f"Result: {result}")

                query_mock.return_value.filter().offset().limit().assert_called_once_with(user=self.user)



    async def test_create_contact(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = None
        result = await create_contact(body=self.body, user=self.user, db=self.session)
        self.assertEqual(result.name, self.body.name)
        self.assertEqual(result.lastname, self.body.lastname)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.phone, self.body.phone)
        # self.assertEqual(result.age, self.body.age)
        # self.assertEqual(result.description, self.body.description)
        self.assertTrue(hasattr(result, "id"))


    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_update_contact_found(self):
            # Визначення
            contact = Contact()
            db_mock = MagicMock()
            db_mock.commit.return_value = None
            self.session.query().filter().filter().first.return_value = contact

            # Коли
            with patch("src.repository.contacts.Session", return_value=db_mock):
                result = await update_contact(
                    contact_id=contact.id,
                    body=self.body,
                    user=self.user,
                    db=self.session,
                )

            # Then
            self.assertEqual(result, contact)  # Очікуваний результат
            db_mock.commit.assert_called_once()  # чи був виклик один раз
            logging.info(f"Result: {result}")

    # async def test_update_contact_found(self):
    #     # Визначення
    #     contact = Contact()
    #     db_mock = AsyncSession()
    #     # db_mock.commit.return_value = None
    #     db_mock.commit.return_value = await asyncio.Future()

    #     self.session.query().filter().filter().first.return_value = contact

    #     # Коли
    #     with patch("sqlalchemy.ext.asyncio.AsyncSession", return_value=db_mock):
    #         result = await update_contact(
    #             contact_id=contact.id,
    #             body=self.body,
    #             user=self.user,
    #             db=self.session,
    #         )

    #     # Then
    #     self.assertEqual(result, contact)  
    #     db_mock.commit.assert_called_once() 
    #     logging.info(f"Result: {result}")



    async def test_get_week_birthdays(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_week_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_search_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().all.return_value = contacts
        result = await search_contacts(user=self.user, db=self.session, search_key="John")
        self.assertEqual(result, contacts)

if __name__ == '__main__':
    unittest.main()