import os
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
import certifi
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")

env = Environment(loader=FileSystemLoader("app/templates"))


async def send_email(to_email: str, subject: str, name: str):

    template = env.get_template("welcome.html")

    html_content = template.render(
        name=name
    )

    message = MIMEMultipart("alternative")
    message["From"] = SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(html_content, "html"))

    tls_context = ssl.create_default_context(cafile=certifi.where())

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        tls_context=tls_context,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
    )