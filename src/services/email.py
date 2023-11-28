import os
from pathlib import Path
from dotenv import load_dotenv
import socket
# from typing import Union


from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service

load_dotenv()

conf = ConnectionConfig(
	MAIL_USERNAME=os.environ['MAIL_USERNAME'],
	MAIL_PASSWORD=os.environ['MAIL_PASSWORD'],
	MAIL_FROM=os.environ['MAIL_FROM'],
	MAIL_PORT=os.environ['MAIL_PORT'],
	MAIL_SERVER=os.environ['MAIL_SERVER'],
	MAIL_FROM_NAME="django.mail.backends.smtp.EmailBackend", #"From future Python developers"
	MAIL_STARTTLS=False,
	MAIL_SSL_TLS=True,
	USE_CREDENTIALS=True,
	VALIDATE_CERTS=True,
	TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
	)
print(Path(__file__).parent / 'templates')


def check_port(host: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  
    try:
        sock.connect((host, port))
        print(f"Порт {port} на хості {host} доступний.")
    except socket.error:
        print(f"Порт {port} на хості {host} недоступний.")
    finally:
        sock.close()
check_port(conf.MAIL_SERVER, conf.MAIL_PORT)


async def send_email(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, 
                           "username": username, 
                           "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)



# future requirements: 
# refactoring script def send_email on two def password_reset and verification