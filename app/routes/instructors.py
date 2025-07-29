from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.instructors import InstructorCreate, InstructorUpdate, InstructorOut
from app.services import instructors as instructor_service

router = APIRouter(prefix="/instructors", tags=["Instructors"])

@router.post("/", response_model=InstructorOut)
def create(data: InstructorCreate, db: Session = Depends(get_db)):
    return instructor_service.create_instructor(db, data)

@router.get("/", response_model=list[InstructorOut])
def get_all(db: Session = Depends(get_db)):
    return instructor_service.get_all_instructors(db)

@router.get("/{instructor_id}", response_model=InstructorOut)
def get_one(instructor_id: int, db: Session = Depends(get_db)):
    instructor = instructor_service.get_instructor_by_id(db, instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@router.put("/{instructor_id}", response_model=InstructorOut)
def update(instructor_id: int, data: InstructorUpdate, db: Session = Depends(get_db)):
    instructor = instructor_service.update_instructor(db, instructor_id, data)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@router.delete("/{instructor_id}")
def delete(instructor_id: int, db: Session = Depends(get_db)):
    deleted = instructor_service.delete_instructor(db, instructor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"detail": "Instructor deleted successfully"}
