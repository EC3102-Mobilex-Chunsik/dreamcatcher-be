from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import queries, models, schemas
from typing import List
from database.connection import SessionLocal, engine

# Configure API router
router = APIRouter(
    tags=['dreams'],
)


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dream database 관련 엔드포인트
@router.post("/dreams", response_model=schemas.Dream)
def create_dream(dream: schemas.DreamCreate, db: Session = Depends(get_db)):
    return queries.create_dream(db=db, dream=dream)


@router.get("/dreams", response_model=List[schemas.Dream])
def read_dreams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dreams = queries.get_dreams(db, skip=skip, limit=limit)
    return dreams


@router.get("/dreams/{dream_id}", response_model=schemas.Dream)
def read_dream(dream_id: int, db: Session = Depends(get_db)):
    db_dream = queries.get_dream(db, dream_id=dream_id)
    if db_dream is None:
        raise HTTPException(status_code=404, detail="Dream not found")
    return db_dream


@router.get("/dreams/{dream_id}/factors/", response_model=List[schemas.DreamFactor])
def read_dream_factors(dream_id: int, db: Session = Depends(get_db)):
    factors = queries.get_dream_factors(db, dream_id=dream_id)
    return factors


@router.get("/dreams/{dream_id}/images/", response_model=List[schemas.DreamImage])
def read_dream_images(dream_id: int, db: Session = Depends(get_db)):
    images = queries.get_dream_images(db, dream_id=dream_id)
    return images
