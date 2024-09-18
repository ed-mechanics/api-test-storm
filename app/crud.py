from sqlalchemy.orm import Session
from app import models, schemas

def get_endpoint(db: Session, endpoint_id: int):
    return db.query(models.Endpoint).filter(models.Endpoint.id == endpoint_id).first()

def get_endpoints(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Endpoint).offset(skip).limit(limit).all()

def create_endpoint(db: Session, endpoint: schemas.EndpointCreate):
    db_endpoint = models.Endpoint(**endpoint.model_dump())
    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint

def get_step(db: Session, step_id: int):
    return db.query(models.Step).filter(models.Step.id == step_id).first()

def create_step(db: Session, step: schemas.StepCreate):
    db_step = models.Step(**step.model_dump())
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

def get_test(db: Session, test_id: int):
    return db.query(models.DatabaseTest).filter(models.DatabaseTest.id == test_id).first()

def create_test(db: Session, test: schemas.TestCreate):
    db_steps = db.query(models.Step).filter(models.Step.id.in_(test.steps)).all()
    db_test = models.DatabaseTest(
        name=test.name,
        description=test.description,
        steps=db_steps,
        allure_feature=test.allure_feature,
        allure_story=test.allure_story,
        allure_epic=test.allure_epic,
        allure_description=test.allure_description
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def update_test(db: Session, test_id: int, test: schemas.TestCreate):
    db_test = db.query(models.DatabaseTest).filter(models.DatabaseTest.id == test_id).first()
    if db_test is None:
        return None
    for key, value in test.model_dump().items():
        if key == "steps":
            db_steps = db.query(models.Step).filter(models.Step.id.in_(value)).all()
            setattr(db_test, key, db_steps)
        else:
            setattr(db_test, key, value)
    db.commit()
    db.refresh(db_test)
    return db_test
