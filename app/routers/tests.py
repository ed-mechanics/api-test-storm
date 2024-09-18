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

@router.post("/tests/", response_model=schemas.Test)
def create_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    db_test = crud.create_test(db=db, test=test)
    return db_test

@router.get("/tests/{test_id}", response_model=schemas.Test)
def read_test(test_id: int, db: Session = Depends(get_db)):
    db_test = crud.get_test(db, test_id=test_id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test
