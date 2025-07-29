# Fitness Class Booking App (Timezone-Aware) - FastAPI + Jinja2

 A booking system where users can schedule fitness classes based on their local timezone. Admins create class slots in IST, and users worldwide see and book in their local time. Bookings close 1 hour before class start.

## Features

- FastAPI backend with Jinja2 templating
- Timezone-aware class booking form (auto-adjusts per browser timezone)
- Booking cutoff: 1 hour before class starts
- Sample input and seed data
- Works with SQLite or PostgreSQL
- Fully tested with cURL & Postman examples

## Setup Instructions

# Project Structure
fitness-booking-app/
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── db/
├── templates/
│   └── booking_form.html
├── README.md
└── requirements.txt

# 1. Clone or Download

```bash
git clone https://github.com/yourusername/fitness-booking-timezone.git
cd fitness-booking-timezone

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload

# Add Instructor
curl -X POST http://127.0.0.1:8000/instructors/ \
-H "Content-Type: application/json" \
-d '{
  "name": "string",
  "phone_number": "string",
  "user_email": "string",
  "id": 0
}'

# Add Fitness Class (Created in IST)
curl -X POST http://127.0.0.1:8000/fitness_classes/ \
-H "Content-Type: application/json" \
-d '{
  "name": "Zumba",
  "total_slots": 10,
  "available_slots": 10,
  "date": "2025-07-31T05:38:08.782Z",  # UTC Time
  "instructor_id": 1
}'

# Book a Slot using cURL:
curl -X POST http://127.0.0.1:8000/bookings/submit \
  -F "client_name=Rahul" \
  -F "client_email=rahul@example.com" \
  -F "fitness_class_id=2" \
  -F "booking_date=2025-07-30T23:08:00Z" \
  -F "timezone=Asia/Kolkata"

POST /bookings/submit
Content-Type: multipart/form-data

{
  "client_name": "Rahul",
  "client_email": "rahul@example.com",
  "fitness_class_id": 2,
  "booking_date": "2025-07-30T23:08:00Z",
  "timezone": "Asia/Kolkata"
}