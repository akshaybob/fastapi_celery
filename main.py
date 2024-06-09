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


@app.get("/legitimate_sellers", response_model=List[LegitimateSellerModel])
async def get_legitimate_sellers(domain: str, db: Session = Depends(get_db)):
    return db.query(LegitimateSeller).filter(LegitimateSeller.domain == domain).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
