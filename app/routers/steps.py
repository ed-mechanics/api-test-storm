from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/steps/", response_model=schemas.Step)
def create_step(step: schemas.StepCreate, db: Session = Depends(get_db)):
    db_step = crud.create_step(db=db, step=step)
    return db_step

@router.get("/steps/{step_id}", response_model=schemas.Step)
def read_step(step_id: int, db: Session = Depends(get_db)):
    db_step = crud.get_step(db, step_id=step_id)
    if db_step is None:
        raise HTTPException(status_code=404, detail="Step not found")
    return db_step
