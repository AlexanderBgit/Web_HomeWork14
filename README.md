
Примітка з ДЗ-14
1.
За допомогою Sphinx додайте в основних модулях до необхідних функцій і методів класів рядки docstrings.

Docstring будується за допомогою плагіну Trelent
Write Docstring | Trelent is bound to Alt + D (⌘ + D on Mac).

2.
Покрийте тестами модулі репозиторію, використовуючи фреймворк Unittest. 

3.
Покрийте функціональними тестами будь-який маршрут на вибір, використовуючи фреймворк pytest.



Примітка з ДЗ-13
Забезпечення конфіденційності
ENV file

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=
SECRET_KEY_JWT=
ALGORITHM=

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

REDIS_HOST=
REDIS={redis port}


Примітка з ДЗ-12
    PostgreSQL database info
    Run uvicorn main:app --reload --host localhost --port 8000 --reload.
    Go to http://127.0.0.1:8000/docs to work with Swagger documentation.
    Аутентифікація наявна 
    Механізм авторизації за допомогою  JWT токенів: access_token та refresh_token

ПРИМІТКА Не забудьте підняти докер-контейнер з PostgreSQL і створити в ньому базу даних

alembic init alembic alembic revision --autogenerate -m 'Init' alembic upgrade head

Docker docker-compose up -d