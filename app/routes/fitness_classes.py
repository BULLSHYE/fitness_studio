from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.fitness_classes import FitnessClassCreate, FitnessClassOut, FitnessClassUpdate
from app.services.fitness_classes import (
    create_fitness_class,
    list_fitness_classes,
    get_fitness_class_by_id,
    update_fitness_class,
    delete_fitness_class_by_id
)
from fastapi import Query
from zoneinfo import ZoneInfo
from typing import Optional

router = APIRouter(prefix="/fitness_classes", tags=["Fitness Classes"])

@router.post("/", response_model=FitnessClassOut)
def create_fitness_class_handler(fitness_class: FitnessClassCreate, db: Session = Depends(get_db)):
    return create_fitness_class(db, fitness_class)

@router.get("/", response_model=list[FitnessClassOut])
def get_fitness_classes(
    db: Session = Depends(get_db),
    tz: Optional[str] = Query(default="Asia/Kolkata")
):
    classes = list_fitness_classes(db)
    try:
        tzinfo = ZoneInfo(tz)
    except Exception:
        tzinfo = ZoneInfo("UTC")

    # Convert UTC to target timezone
    for fc in classes:
        if fc.date.tzinfo is None:
            fc.date = fc.date.replace(tzinfo=ZoneInfo("UTC"))
        fc.date = fc.date.astimezone(tzinfo)
    return classes
@router.get("/{class_id}", response_model=FitnessClassOut)
def get_fitness_class_handler(class_id: int, db: Session = Depends(get_db)):
    fitness_class = get_fitness_class_by_id(db, class_id)
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Fitness class not found")
    return fitness_class

@router.put("/{class_id}", response_model=FitnessClassOut)
def update_fitness_class_handler(class_id: int, updates: FitnessClassUpdate, db: Session = Depends(get_db)):
    updated = update_fitness_class(db, class_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Fitness class not found")
    return updated

@router.delete("/{class_id}")
def delete_fitness_class_handler(class_id: int, db: Session = Depends(get_db)):
    deleted = delete_fitness_class_by_id(db, class_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fitness class not found")
    return {"detail": "Fitness class deleted successfully"}
