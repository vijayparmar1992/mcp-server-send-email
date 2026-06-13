from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    to: list[EmailStr] = Field(..., description="List of recipient email addresses")
    subject: str = Field(..., min_length=1, description="Subject of the email")
    message: str = Field(..., min_length=1, description="Body of the email")
    cc: list[EmailStr] = []
    bcc: list[EmailStr] = []
    reply_to: EmailStr | None = None


class EmailResponse(BaseModel):
    status: str
    to: list[str]
    subject: str
    message_id: str | None = None
    detail: str
