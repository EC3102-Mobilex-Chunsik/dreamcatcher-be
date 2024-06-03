from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class DreamFactorBase(BaseModel):
    tagName: str
    description: str


class DreamFactorCreate(DreamFactorBase):
    pass


class DreamFactor(DreamFactorBase):
    factor_id: int
    dream_id: int

    class Config:
        orm_mode = True


class DreamImageBase(BaseModel):
    url: str


class DreamImageCreate(DreamImageBase):
    pass


class DreamImage(DreamImageBase):
    image_id: int
    dream_id: int

    class Config:
        orm_mode = True


class DreamBase(BaseModel):
    dateTime: datetime
    title: str
    inputPrompt: str
    context: str


class DreamCreate(DreamBase):
    factors: List[DreamFactorCreate]
    images: List[DreamImageCreate]


class Dream(DreamBase):
    id: int
    factors: List[DreamFactor] = []
    images: List[DreamImage] = []

    class Config:
        orm_mode = True
