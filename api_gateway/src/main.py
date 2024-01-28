from fastapi import FastAPI
from routers import travel_plans, primary

app = FastAPI()
app.include_router(travel_plans.router)
app.include_router(primary.router)