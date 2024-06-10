""" modules deals with DB connection """

import os
from sqlalchemy import create_engine, Column, String, Date, DateTime, Enum, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

DATABASE_URL =os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
