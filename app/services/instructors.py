from sqlalchemy.orm import Session
from app.models.instructors import Instructor
from app.schemas.instructors import InstructorCreate, InstructorUpdate

def create_instructor(db: Session, data: InstructorCreate):
    instructor = Instructor(**data.dict())
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor

def get_all_instructors(db: Session):
    return db.query(Instructor).all()

def get_instructor_by_id(db: Session, instructor_id: int):
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()

def delete_instructor(db: Session, instructor_id: int):
    instructor = get_instructor_by_id(db, instructor_id)
    if instructor:
        db.delete(instructor)
        db.commit()
    return instructor

def update_instructor(db: Session, instructor_id: int, data: InstructorUpdate):
    instructor = get_instructor_by_id(db, instructor_id)
    if not instructor:
        return None
    for key, value in data.dict().items():
        setattr(instructor, key, value)
    db.commit()
    db.refresh(instructor)
    return instructor
