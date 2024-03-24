from pydantic import BaseModel


class EmailRequest(BaseModel):
    sender_email: str
    sender_password: str
    recipient_email: str
    subject: str
    body: str