import os
import smtplib
from email.message import EmailMessage
from .models import EmailRequest, EmailResponse
from dotenv import load_dotenv

load_dotenv()

def send_email(request: EmailRequest) -> EmailResponse:
    smtp_host = os.getenv("SMTP_HOST", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from = os.getenv("SMTP_FROM", "")
    smtp_starttls = os.getenv("SMTP_STARTTLS", "true").lower() == "true"

    if not smtp_from:
        return EmailResponse(
            status="error",
            to=[str(email) for email in request.to],
            subject=request.subject,
            detail="SMTP_FROM environment variable is not set",
        )

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = ", ".join(str(email) for email in request.to)
    msg["Subject"] = request.subject

    if request.cc:
        msg["Cc"] = ", ".join(str(email) for email in request.cc)

    if request.reply_to:
        msg["Reply-To"] = str(request.reply_to)

    msg.set_content(request.message)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
            if smtp_starttls:
                smtp.starttls()

            if smtp_username and smtp_password:
                smtp.login(smtp_username, smtp_password)

            smtp.send_message(msg)

        return EmailResponse(
            status="sent",
            to=[str(email) for email in request.to],
            subject=request.subject,
            detail="Email sent successfully.",
        )
    except Exception as e:
        return EmailResponse(
            status="error",
            to=[str(email) for email in request.to],
            subject=request.subject,
            detail=f"Failed to send email: {str(e)}",
        )

