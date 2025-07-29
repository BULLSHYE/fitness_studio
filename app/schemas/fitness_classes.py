from pydantic import BaseModel, validator
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

class FitnessClassBase(BaseModel):
    name: str
    total_slots: int
    available_slots: int
    date: datetime
    instructor_id: int

class FitnessClassCreate(FitnessClassBase):
    pass

class FitnessClassUpdate(BaseModel):
    name: Optional[str] = None
    total_slots: Optional[int] = None
    available_slots: Optional[int] = None
    date: Optional[datetime] = None
    instructor_id: Optional[int] = None

class FitnessClassOut(FitnessClassBase):
    id: int

    class Config:
        orm_mode = True
