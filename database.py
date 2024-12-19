import os 
from sqlalchemy import Column, Integer, String, DateTime, create_engine 
from sqlalchemy.orm import Session, sessionmaker, declarative_base 
from dotenv import load_dotenv 
from models import Event

load_dotenv() 
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mariawasnotfound:0000@localhost:5432/afisha_db") 
 
Base = declarative_base() 
engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
 
def save_event(title, location, latitude, longitude, start_time, availability_status, link):
    db: Session = SessionLocal()
    try:
        new_event = Event(
            title=title,
            location=location,
            latitude=latitude,
            longitude=longitude,
            start_time=start_time,
            availability_status=availability_status,
            link=link
        )
        db.add(new_event)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении события: {e}")
    finally:
        db.close()
 
def init_db():  
   Base.metadata.create_all(bind=engine) 
 
if __name__ == "__main__": 
    init_db()
