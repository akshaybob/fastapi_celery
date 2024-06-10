"""Module delas with Table Model structure """
import uuid
from sqlalchemy import create_engine, Column, String, Date, DateTime, Enum, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum
from database import Base


class TaskStatus(enum.Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'


class Task(Base):
    _tablename_ = 'tasks'
    run_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, default=datetime.utcnow().date())
    status = Column(Enum(TaskStatus), default=TaskStatus.SCHEDULED)
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
    
