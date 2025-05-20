import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
email_correo = os.getenv("USER_EMAIL")
password = os.getenv("USER_PASS")


def send_email(subject, body, to_email):
    email = MIMEMultipart()
    email["From"] = email_correo
    email["To"] = to_email
    email["Subject"] = subject
    email.attach(MIMEText(body, "plain"))

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(email_correo, password)

    servidor.send_message(email)
    servidor.quit()
    print("Correo enviado con exito")
