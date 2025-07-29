from sqlalchemy.orm import Session
from app.models.fitness_classes import FitnessClass
from app.schemas.fitness_classes import FitnessClassCreate, FitnessClassUpdate
from pytz import timezone
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

def create_fitness_class(db: Session, fitness_class_data: FitnessClassCreate):
    data = fitness_class_data.dict()
    if data.get("date"):
        # Always store in UTC
        date = data["date"]
        if date.tzinfo is None:
            date = date.replace(tzinfo=ZoneInfo("UTC"))
        else:
            date = date.astimezone(ZoneInfo("UTC"))
        data["date"] = date
    fitness_class = FitnessClass(**data)
    db.add(fitness_class)
    db.commit()
    db.refresh(fitness_class)
    return fitness_class

def list_fitness_classes(db: Session):
    return db.query(FitnessClass).all()

def get_fitness_class_by_id(db: Session, class_id: int):
    return db.query(FitnessClass).filter(FitnessClass.id == class_id).first()

def update_fitness_class(db: Session, class_id: int, updates: FitnessClassUpdate):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
    if not fitness_class:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(fitness_class, key, value)
    db.commit()
    db.refresh(fitness_class)
    return fitness_class

def delete_fitness_class_by_id(db: Session, class_id: int):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
    if fitness_class:
        db.delete(fitness_class)
        db.commit()
    return fitness_class
