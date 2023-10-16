# Nadefinujeme objekty pro tabulky
# pydantic vyuziva typovani pro jednodussi tvorbu objektu

from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

class Bed(BaseModel):
    type: str

class MedicalExam(BaseModel):
    datetime: datetime
    doctor: str
    report: str

class Pet(BaseModel):
    id: UUID
    name: str
    registration: date | None
    bed: Bed | None
    medical_exam: list[MedicalExam]