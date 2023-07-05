# authentication/utils.py

import jwt
from .settings import env
import smtplib
from email.message import EmailMessage

def generate_jwt_token(payload):
    token = jwt.encode(payload, env("JWT_SECRET_KEY"), algorithm='HS256')
    return token.decode('utf-8')

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, env("JWT_SECRET_KEY"), algorithms=['HS256'])
        return decoded_payload
    except jwt.DecodeError:
        return None

def send_email(to_email:str, body: str, subject:str, from_email:str=env("SENDER_EMAIL_ID")):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(env("SENDER_EMAIL_ID"), env("SENDER_EMAIL_APP_PASSWORD"))
    
    # message to be sent
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email
    message.set_content(body)
    # sending the mail
    s.send_message(message)
    # terminating the session
    s.quit()