import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv("email")
password = os.getenv("pass")


def send_email(subject, body, to_email):
    email = EmailMessage()
    email["From"] = email
    email["To"] = to_email
    email["Subject"] = subject
    email.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(email)
