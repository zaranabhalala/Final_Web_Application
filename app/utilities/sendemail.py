import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def absolute_path(filepath):
    relative = Path(filepath)
    return relative.absolute()


def sendemail(to, strHash):
    sender_email = "jmnjit3@gmail.com"
    receiver_email = to
    password = 'Qwerty123$'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify email for MLB Player's database access"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hi,
    You have Sign Up for the MLB Player's database.
    Please click on link to verify email."""

    html = """\
    <html>
      <body>
        <p>Hi,<br>
           You have Sign Up for the MLB Player's database.<br><br>
           <a href="http://0.0.0.0:5000/validateLogin/""""" + strHash + """">Click Here</a> 
           to validate your email address.
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        server.quit()
