# authentication/utils.py

import jwt
from .settings import env
import smtplib
from email.message import EmailMessage
from deepface import DeepFace
import base64
import json
from django.core import serializers
from fpdf import FPDF
import cloudinary
import cloudinary.uploader

def convert_image_to_base64(image_data):
    encoded_string = base64.b64encode(image_data)
    return encoded_string.decode('utf-8')

def verify_user(img1:str, img2:str, model_name:str="Facenet512"):
    result = DeepFace.verify(img1_path = img1, img2_path = img2, model_name=model_name)
    return result


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
    
def convert_json_to_pdf_and_upload(json_data):
    print(json_data)
    listData = list(json_data)
    jsonData = json.dumps(listData)
    data = json.loads(jsonData)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    
    headers = list(data[0].keys())
    table_width = pdf.w - 2 * pdf.l_margin
    col_width = table_width / len(headers)
    row_height = pdf.font_size + 4

    # Set table header style
    pdf.set_fill_color(52, 73, 94)  # Dark blue
    pdf.set_text_color(255, 255, 255)  # White

    # Add table headers
    for header in headers:
        pdf.cell(col_width, row_height, txt=header, border=1, fill=True, align='C')
    pdf.ln(row_height)

    # Set table body style
    pdf.set_fill_color(236, 240, 241)  # Light gray
    pdf.set_text_color(0, 0, 0)  # Black

    # Add table rows
    for item in data:
        for value in item.values():
            pdf.cell(col_width, row_height, txt=str(value), border=1, fill=True, align='C')
        pdf.ln(row_height)

    # Get the byte data of the PDF
    pdf_data = pdf.output(dest='S').encode('latin-1')

    # Upload the PDF data to Cloudinary
    response = cloudinary.uploader.upload(pdf_data, resource_type='auto')

    # Return the Cloudinary URL of the uploaded PDF
    return response['secure_url']   
