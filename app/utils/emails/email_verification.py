import smtplib

import os
import time
import jwt
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import settings

async def send_verification_email(username:str,email:str):
    payload:dict={
        "username":username,
        "email":email,
        "exp":time.time()+ (60*60)
    }
    __token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.HASHING_ALGORITHM)
    template_path = "templates/email_verification.html"
    with open(template_path,'r') as html_file:
        content = html_file.read()

    html_content_with_token =  content.replace("{{token}}", __token).replace("{{username}}",username).replace('{{BASE_URL}}',settings.BASE_URL)


    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_USERNAME
    msg["To"] = email
    msg['Subject'] = 'qamqor.kz account verification'
    msg.attach(MIMEText(html_content_with_token, "html"))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(settings.EMAIL_USERNAME,settings.EMAIL_PASSWORD)
            smtp.send_message(msg)
        print('Sended')
    except Exception as e:
        error_message = f"Failed to send email: {str(e)}"
        print(error_message)
        return {"error": error_message}