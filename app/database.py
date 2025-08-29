from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer

from fastapi import FastAPI

DATABASE_URL = 'mysql+pymysql://user:password@db:3306/fastapi_db'
engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase): pass
class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    number = Column(String(12))

SessionLocal = sessionmaker(autoflush=False, bind=engine)