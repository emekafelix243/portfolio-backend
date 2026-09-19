from pydantic import BaseModel, EmailStr
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactResponse(ContactCreate):
    id: int
    created_at: datetime
    is_read: bool

    class Config:
        from_attributes = True
