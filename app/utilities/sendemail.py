import smtplib
import ssl
from pathlib import Path


def absolute_path(filepath):
    password = '12345678'
    relative = Path(filepath)
    return relative.absolute()


def sendemail(to):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "zaranabhalala1996@gmail.com"  # Enter your address
    receiver_email = to  # Enter receiver address
    password = '12345678'
    message = """\
    Subject: Hi there
    This message is sent from MLB Player's Team"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)