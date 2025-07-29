
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
connection_string = os.getenv("DATABASE_CONNECTION_STRING")


engine = create_engine(connection_string)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
