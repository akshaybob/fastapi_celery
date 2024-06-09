import os
import uuid
from sqlalchemy import create_engine, Column, String, Date, DateTime, Enum, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Task(Base):
    _tablename_ = 'tasks'
    run_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, default=datetime.utcnow().date())
    status = Column(String(30))
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    legitimate_sellers = relationship('LegitimateSeller', back_populates='task')


class LegitimateSeller(Base):
    _tablename_ = 'legitimate_sellers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column(String(500))#100
    ssp_domain_name = Column(String(500))#200
    publisher_id = Column(String(500))#200
    seller_relationship = Column(String(500))#50
    date = Column(Date, default=datetime.utcnow().date())
    run_id = Column(String(200), ForeignKey('tasks.run_id'))# 30
    task = relationship('Task', back_populates='legitimate_sellers')


DATABASE_URL =os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


class TaskModel(PydanticBaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = Field(default_factory=datetime.utcnow)
    status: str
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LegitimateSellerModel(PydanticBaseModel):
    id: int
    site: str
    ssp_domain_name: str
    publisher_id: str
    seller_relationship: str
    date: datetime = Field(default_factory=datetime.utcnow)
    run_id: str

    class Config:
        from_attributes = True
