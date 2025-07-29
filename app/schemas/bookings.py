from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    client_name: str
    client_email: EmailStr
    fitness_class_id: int

class BookingCreate(BookingBase):
    booking_date: datetime
    # pass

class BookingUpdate(BaseModel):
    status: Optional[str] = None

class Booking(BookingBase):
    id: int
    booking_date: datetime
    status: str

    class Config:
        orm_mode = True
