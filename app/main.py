from fastapi import FastAPI
from app.db.db import Base, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from app.routes.instructors import router as instructors_router
from app.routes.fitness_classes import router as fitness_classes_router
from app.routes.bookings import router as bookings_router
import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import inspect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()
inspector = inspect(engine)
print(inspector.get_table_names())
Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(instructors_router)
app.include_router(fitness_classes_router)
app.include_router(bookings_router)

@app.get("/")
async def root():
    return {"message": "API is running", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)