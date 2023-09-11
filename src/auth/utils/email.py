import os
from pathlib import Path

from fastapi_mail import FastMail, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.config import settings

from fastapi_mail import MessageSchema

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent.parent / "templates",
)


async def send_email_for_reset_pswd(
    email: EmailStr, username: str, reset_token: str, host: str
):
    try:
        message = MessageSchema(
            subject="Password change",
            recipients=[email],
            template_body={"host": host, "username": username, "token": reset_token},
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password.html")

    except ConnectionErrors as e:
        print(e)


async def send_email_verification(
    email: EmailStr, username: str, verify_token: str, host: str
):
    try:
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": verify_token},
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_verification.html")
    except ConnectionErrors as e:
        print(e)
