
# Примітка з ДЗ-14



## 1.
- [x] За допомогою **Sphinx** додано в основних модулях /функціях і методів класів рядки docstrings.

Docstring будується за допомогою плагіну **Trelent**
Write Docstring | Trelent is bound to **Alt + D** (⌘ + D on Mac).

## 2.
- [x] Покриті тестами модулі репозиторію, використовуючи фреймворк **Unittest**. 

## 3.
- [x] Покриті функціональними тестами маршрут ***на вибір***, використовуючи фреймворк **pytest**.



# Примітка з ДЗ-13


## Забезпечення конфіденційності
```
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
```

# Примітка з ДЗ-12


    PostgreSQL database info
    
    Run uvicorn main:app --reload --host localhost --port 8000 --reload.
    Go to http://127.0.0.1:8000/docs to work with Swagger documentation.
    
    Аутентифікація наявна 
    
    Механізм авторизації за допомогою  JWT токенів: access_token та refresh_token

#### ПРИМІТКА Не забудьте підняти докер-контейнер з PostgreSQL і створити в ньому базу даних

>alembic init alembic alembic revision --autogenerate -m 'Init' alembic upgrade head

>Docker docker-compose up -d



## Документація коду проекту

![Rest API](https://github.com/AlexanderBgit/Web_HomeWork14/blob/e5cef0943dabc3745c70e08200a1632e0b75979d/_png/Rest%20API%2014.0%20documentation.png?raw=true)
