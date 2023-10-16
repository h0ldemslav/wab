from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Bed(Base):
    __tablename__ = "beds"

    id = Column(UUID, primary_key=True, index=True)
    type = Column(String)
    pet_id = Column(UUID, ForeignKey("pets.id"))

class MedicalExam(Base):
    __tablename__ = "medical_exams"

    id = Column(UUID, primary_key=True, index=True)
    datetime = Column(DateTime)
    doctor = Column(String)
    report = Column(String)
    pet_id = Column(UUID, ForeignKey("pets.id"))

class Pet(Base):
    __tablename__ = "pets"

    id = Column(UUID, primary_key=True, index=True) 
    name = Column(String)
    registration = Column(DateTime, nullable=True)
    bed = relationship("Bed")
    medical_exam = relationship("MedicalExam")