from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from database.connection import Base


class Dream(Base):
    __tablename__ = "dreams"

    id = Column(Integer, primary_key=True)
    dateTime = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    inputPrompt = Column(Text, nullable=False)
    context = Column(Text, nullable=False)

    factors = relationship(
        "DreamFactor", back_populates="dream", cascade="all, delete-orphan")
    images = relationship(
        "DreamImage", back_populates="dream", cascade="all, delete-orphan")


class DreamFactor(Base):
    __tablename__ = "dream_factors"

    factor_id = Column(Integer, primary_key=True)
    dream_id = Column(Integer, ForeignKey("dreams.id"), nullable=False)
    tagName = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    dream = relationship("Dream", back_populates="factors")


class DreamImage(Base):
    __tablename__ = "dream_images"

    image_id = Column(Integer, primary_key=True)
    dream_id = Column(Integer, ForeignKey("dreams.id"), nullable=False)
    url = Column(String, nullable=False)

    dream = relationship("Dream", back_populates="images")
