from pydantic import BaseModel
from typing import Optional

class InstructorBase(BaseModel):
    name: str
    phone_number: str
    user_email: str

class InstructorCreate(InstructorBase):
    pass

class InstructorUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    user_email: Optional[str] = None

class InstructorOut(InstructorBase):
    id: int

    class Config:
        orm_mode = True