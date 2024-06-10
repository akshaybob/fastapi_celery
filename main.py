from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Task, LegitimateSeller, Base, TaskModel, LegitimateSellerModel, SessionLocal
from typing import List
from datetime import datetime

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasksdate", response_model=List[TaskModel])
async def get_tasks_by_date(date: datetime, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.date == date).all()


@app.get("/legitimate_sellers", response_model=List[LegitimateSellerModel])
async def get_legitimate_sellers(domain: str, db: Session = Depends(get_db)):
    return db.query(LegitimateSeller).filter(LegitimateSeller.domain == domain).all()


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
