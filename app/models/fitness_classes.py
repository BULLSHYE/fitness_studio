from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime

class FitnessClass(Base):
    __tablename__ = 'fitness_classes'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    instructor_id = Column(Integer, ForeignKey('instructors.id'), nullable=False)

    instructor = relationship("Instructor", back_populates="fitness_classes")
    bookings = relationship("Booking", back_populates="fitness_class")
