"""Module deals with running project for expossing Api's"""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import  TaskModel, LegitimateSellerModel
from typing import List
from datetime import datetime
from database import get_db

from database import engine, Base
from models import Task, LegitimateSeller

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasksdate", response_model=List[TaskModel])
async def get_tasks_by_date(date: datetime, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.date == date).all()


@app.get("/legitimate_sellers", response_model=List[LegitimateSellerModel])
async def get_legitimate_sellers(domain: str, db: Session = Depends(get_db)):
    return db.query(LegitimateSeller).filter(LegitimateSeller.ssp_domain_name == domain).all()


@app.get("/stats")
async def get_stats(from_date: datetime, to_date: datetime, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.finished_at.between(from_date, to_date)).all()
    execution_times = [(task.finished_at - task.started_at).total_seconds() for task in tasks
                       if task.finished_at and task.started_at]
    if not execution_times:
        return {"average_execution_time": 0}
    return {"average_execution_time": sum(execution_times) / len(execution_times)}

if _name_ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)

