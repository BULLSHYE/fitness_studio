from sqlalchemy.orm import Session
from app.models.bookings import Booking
from app.schemas.bookings import BookingCreate
from app.services.fitness_classes import get_fitness_class_by_id
from datetime import datetime, timedelta
import pytz
from zoneinfo import ZoneInfo

ist = pytz.timezone("Asia/Kolkata")

def create_booking_html(db: Session, booking_data: BookingCreate):
    fitness_class = get_fitness_class_by_id(db, booking_data.fitness_class_id)
    if not fitness_class:
        raise ValueError("Invalid class")

    now_utc = datetime.utcnow().replace(tzinfo=ZoneInfo("UTC"))
    event_time = fitness_class.date.astimezone(ZoneInfo("UTC"))
    booking_time = booking_data.booking_date.astimezone(ZoneInfo("UTC"))

    if booking_time <= now_utc:
        raise ValueError("You cannot book for a past time.")

    if booking_time >= event_time:
        raise ValueError("You cannot book after the event has started.")

    if (event_time - booking_time).total_seconds() < 3600:
        raise ValueError("Booking must be made at least 1 hour before the event.")

    if fitness_class.available_slots <= 0:
        raise ValueError("No slots available")

    fitness_class.available_slots -= 1
    db.add(fitness_class)
    db.commit()
    db.refresh(fitness_class)

    booking = Booking(**booking_data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking

def create_booking(db: Session, booking_data: BookingCreate):
    fitness_class = get_fitness_class_by_id(db, booking_data.fitness_class_id)
    if not fitness_class:
        raise ValueError("Fitness class does not exist")

    if fitness_class.available_slots <= 0:
        raise ValueError("No slots available for this fitness class")

    # reduce slot
    fitness_class.available_slots -= 1
    db.add(fitness_class)

    booking = Booking(
        **booking_data.dict(),
        booking_date=datetime.now(ist)
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def list_bookings(db: Session):
    return db.query(Booking).all()

def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings_by_email(db: Session, email: str):
    return db.query(Booking).filter(Booking.client_email == email).all()

def get_upcoming_bookings(db: Session, email: str):
    now_ist = datetime.now(ist)
    return db.query(Booking).filter(
        Booking.client_email == email,
        Booking.booking_date >= now_ist
    ).all()
