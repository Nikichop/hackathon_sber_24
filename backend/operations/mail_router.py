# mail_router.py

from fastapi import APIRouter, HTTPException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from operations.schemas import EmailRequest

router = APIRouter(
    prefix="/mail",
    tags=["Mail"]
)


@router.post("/send_email/")
async def send_email(email_request: EmailRequest):
    try:
        # Установка соединения с SMTP-сервером
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_request.sender_email, email_request.sender_password)

        # Создание сообщения
        message = MIMEMultipart()
        message['From'] = email_request.sender_email
        message['To'] = email_request.recipient_email
        message['Subject'] = email_request.subject
        message.attach(MIMEText(email_request.body, 'html'))  # Используем тип html

        # Отправка сообщения
        server.sendmail(email_request.sender_email, email_request.recipient_email, message.as_string())
        server.quit()

        return {"message": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



