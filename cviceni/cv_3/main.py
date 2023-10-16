import database
import models
import domain
from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, Path


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pet")
def get_pets() -> list[models.Pet]:
    pets = database.SessionLocal.begin().query(domain.Pet)

    # ** rozbali zvire a prida do seznamu
    return [models.Pet(**p) for p in pets]

# FastAPI ti automaticky generuje dokumentaci ve Swaggeru, url /docs
@app.get("/pet/{pet_id}")
def get_pets(pet_id: Annotated[UUID, Path(title="The pet id")]) -> models.Pet:
    return pet_id