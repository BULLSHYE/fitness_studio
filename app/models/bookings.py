from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    fitness_class_id = Column(Integer, ForeignKey("fitness_classes.id"))
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")

    fitness_class = relationship("FitnessClass", back_populates="bookings")
