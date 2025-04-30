import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_verification_email(email, verification_code):
    """
    Send a verification email with a token.
    """
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")

    subject = "Verify Your Email - Vetty"
    content = f"""
    <p>Thank you for registering with Vetty!</p>
    <p>Please use the following verification code to verify your email:</p>
    <h3>{verification_code}</h3>
    <p>If you did not request this, please ignore this email.</p>
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(content, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")