import time
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from app.database import *

def wait_for_db():
    engine = create_engine(DATABASE_URL)
    for i in range(10):  # пробуем 10 раз с интервалом 5 секунд
        try:
            with engine.connect() as conn:
                print("✅ Database connection successful!")
                return True
        except OperationalError:
            print(f"⏳ Waiting for database... (attempt {i+1}/10)")
            time.sleep(5)
    raise Exception("❌ Could not connect to database after 10 attempts")

wait_for_db()

Base.metadata.create_all(bind=engine)


app = FastAPI(title = 'Booking API')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def main():
    return FileResponse('app/public/index.html')



@app.get("/health")
def health_check():
    return {"status": "healthy"}