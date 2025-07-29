from sqlalchemy.orm import relationship
from app.db.db import Base
from sqlalchemy import Column, Integer, String

class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_email = Column(String, unique=True)
    phone_number = Column(String)

    fitness_classes = relationship("FitnessClass", back_populates="instructor")