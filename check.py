import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import ssl 

import os
from dotenv import load_dotenv


def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # таймаут на 1 секунду

    try:
        sock.connect((host, port))
        print(f"Порт {port} на хості {host} доступний.")
    except socket.error:
        print(f"Порт {port} на хості {host} недоступний.")
    finally:
        sock.close()

# Перевірка порту
check_port('smtp.meta.ua', 465)
check_port('smtp.meta.ua', 25)
# check_port('smtp.meta.ua', 587)
# check_port('smtp.meta.ua', 2525)
# check_port('smtp.meta.ua', 995)


load_dotenv()

MAIL_STARTTLS = False
MAIL_SSL_TLS = True  # Change if use SSL/TLS
USE_CREDENTIALS = True
VALIDATE_CERTS = True

def check_smtp_connection():
    smtp_username = os.environ['MAIL_USERNAME']
    smtp_password = os.environ['MAIL_PASSWORD']


    smtp_server = os.environ['MAIL_SERVER']
    smtp_port = os.environ['MAIL_PORT']
    sender_email = os.environ['MAIL_FROM']
    receiver_email = 'studrest@meta.ua' # temp-mail.org


    subject = 'Тестове повідомлення'
    body = 'Це тестове повідомлення для перевірки підключення до SMTP-сервера.'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        print(f'Підключення до SMTP-сервера: {smtp_server}:{smtp_port}')
        # print(f'Логін: {smtp_username}, Пароль: {smtp_password}')

        if MAIL_SSL_TLS:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if MAIL_STARTTLS:
                    server.starttls()

                if USE_CREDENTIALS:
                    server.login(smtp_username, smtp_password)

                server.sendmail(sender_email, receiver_email, message.as_string())

        print('Підключення до SMTP-сервера успішно!')
    except Exception as e:
        print(f'Помилка при підключенні до SMTP-сервера: {e}')

# перевірка підключення
check_smtp_connection()
