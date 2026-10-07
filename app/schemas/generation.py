from datetime import date

from pydantic import BaseModel, EmailStr, Field


class Recipient(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr


class GenerationRequest(BaseModel):
    event_name: str = Field(..., min_length=2, max_length=255)
    issue_date: date
    recipients: list[Recipient] = Field(..., min_length=1)