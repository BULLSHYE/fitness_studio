from fastapi import APIRouter, Depends, HTTPException, Query,  Request, Form
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.bookings import BookingCreate, Booking
from app.services.bookings import (
    create_booking, list_bookings,
    get_booking_by_id, get_bookings_by_email,
    get_upcoming_bookings
)
from app.services.fitness_classes import list_fitness_classes, get_fitness_class_by_id
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.bookings import create_booking_html
from datetime import datetime
import pytz 
router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/form", response_class=HTMLResponse)
def booking_form(request: Request, db: Session = Depends(get_db)):
    from app.main import templates
    classes = list_fitness_classes(db)
    return templates.TemplateResponse("booking_form.html", {"request": request, "classes": classes})

@router.post("/submit")
def submit_booking(
    request: Request,
    client_name: str = Form(...),
    client_email: str = Form(...),
    fitness_class_id: int = Form(...),
    booking_date: str = Form(...),  # ISO UTC from frontend
    timezone: str = Form(...),
    db: Session = Depends(get_db),
):
    from app.main import templates
    from zoneinfo import ZoneInfo

    try:
        # Parse ISO date from UTC string
        booking_datetime = datetime.fromisoformat(booking_date)
        if booking_datetime.tzinfo is None:
            booking_datetime = booking_datetime.replace(tzinfo=ZoneInfo("UTC"))
    except ValueError:
        return templates.TemplateResponse("booking_form.html", {
            "request": request,
            "classes": list_fitness_classes(db),
            "error": "Invalid date format.",
        })

    fitness_class = get_fitness_class_by_id(db, fitness_class_id)
    if not fitness_class:
        return templates.TemplateResponse("booking_form.html", {
            "request": request,
            "classes": list_fitness_classes(db),
            "error": "Invalid fitness class selected.",
        })

    booking_data = BookingCreate(
        client_name=client_name,
        client_email=client_email,
        fitness_class_id=fitness_class_id,
        booking_date=booking_datetime,
    )

    try:
        create_booking_html(db, booking_data)
    except ValueError as e:
        return templates.TemplateResponse("booking_form.html", {
            "request": request,
            "classes": list_fitness_classes(db),
            "error": str(e),
        })

    return RedirectResponse("/bookings/form", status_code=303)

@router.get("/", response_model=list[Booking])
def list_all_bookings(db: Session = Depends(get_db)):
    return list_bookings(db)

@router.get("/by-email/", response_model=list[Booking])
def get_bookings_by_email_route(email: str = Query(...), db: Session = Depends(get_db)):
    return get_bookings_by_email(db, email)

@router.get("/upcoming/", response_model=list[Booking])
def get_upcoming_bookings_route(email: str = Query(...), db: Session = Depends(get_db)):
    return get_upcoming_bookings(db, email)
