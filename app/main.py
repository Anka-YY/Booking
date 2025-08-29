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

@app.get('/api/users')
def get_users(db: Session = Depends(get_db)):
    '''Отображение всех пользователей на странице'''
    return db.query(Person).all()

@app.get('/api/users/{id}')
def get_person(id, db: Session = Depends(get_db)):
    '''Получение одного пользователя и возращение его данных'''
    person = db.query(Person).filter(Person.id == id).first()
    if person == None:
        JSONResponse(status_code=404, content={'message': 'Пользователь не найден'})
    return person

@app.post('/api/users')
def create_users(data = Body(), db: Session = Depends(get_db)):
    '''Добавляет пользователя и возвращает его данные'''
    person = Person(name=data['name'], number=data['number'])
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

@app.put('/api/users')
def edit_users(data = Body(), db: Session = Depends(get_db)):
    '''Изменение данных пользователя и возвращение всех пользователей'''
    person = db.query(Person).filter(Person.id == data['id']).first()
    if person == None:
        return JSONResponse(status_code=404, content={'message': 'Пользователь не найден'})
    person.name = data['name']
    person.number = data['number']
    db.commit()
    db.refresh(person)
    return person

@app.delete('/api/users/{id}')
def delete_users(id, db: Session = Depends(get_db)):
    '''Удаление пользователя и возвращение данных без удаленного пользователя'''
    person = db.query(Person).filter(Person.id == id).first()
    if person == None:
        return JSONResponse(status_code=404, content={'message' : 'Пользователь не найден'})
    db.delete(person)
    db.commit()
    return person

@app.get("/health")
def health_check():
    return {"status": "healthy"}