from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from .email_service import send_email

app = FastAPI()


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    name: str


@app.post("/send-email")
async def send_email_api(data: EmailRequest):
    try:
        await send_email(
            to_email=data.to,
            subject=data.subject,
            name=data.name,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to send email: {exc}",
        ) from exc

    return {
        "success": True,
        "message": "Email sent successfully"
    }