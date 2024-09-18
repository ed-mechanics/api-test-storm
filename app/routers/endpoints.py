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

@router.post("/endpoints/", response_model=schemas.Endpoint)
def create_endpoint(endpoint: schemas.EndpointCreate, db: Session = Depends(get_db)):
    db_endpoint = crud.create_endpoint(db=db, endpoint=endpoint)
    return db_endpoint

@router.get("/endpoints/", response_model=List[schemas.Endpoint])
def read_endpoints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    endpoints = crud.get_endpoints(db, skip=skip, limit=limit)
    return endpoints

@router.get("/endpoints/{endpoint_id}", response_model=schemas.Endpoint)
def read_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    db_endpoint = crud.get_endpoint(db, endpoint_id=endpoint_id)
    if db_endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return db_endpoint
