from sqlalchemy.orm import Session
import database.models as models
import database.schemas as schemas


def get_dream(db: Session, dream_id: int):
    return db.query(models.Dream).filter(models.Dream.id == dream_id).first()


def get_dreams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dream).offset(skip).limit(limit).all()


def create_dream(db: Session, dream: schemas.DreamCreate):
    db_dream = models.Dream(
        dateTime=dream.dateTime,
        title=dream.title,
        inputPrompt=dream.inputPrompt,
        context=dream.context
    )
    db.add(db_dream)
    db.commit()
    db.refresh(db_dream)

    for factor in dream.factors:
        db_factor = models.DreamFactor(
            dream_id=db_dream.id,
            tagName=factor.tagName,
            description=factor.description
        )
        db.add(db_factor)

    for image in dream.images:
        db_image = models.DreamImage(
            dream_id=db_dream.id,
            url=image.url
        )
        db.add(db_image)

    db.commit()

    return db_dream


def get_dream_factors(db: Session, dream_id: int):
    return db.query(models.DreamFactor).filter(models.DreamFactor.dream_id == dream_id).all()


def get_dream_images(db: Session, dream_id: int):
    return db.query(models.DreamImage).filter(models.DreamImage.dream_id == dream_id).all()
