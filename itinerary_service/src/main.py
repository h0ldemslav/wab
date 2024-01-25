from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from model import Token, TravelPlanResponse, TravelPlan
from uuid import uuid4
from datetime import datetime

app = FastAPI()
itinerary_routes = {
    "travel_plans": "/travel_plans"
}

@app.post(itinerary_routes["travel_plans"])
async def get_travel_plans(token: Token):
    # TODO: replace fake data with db
    return TravelPlanResponse(data=[
        TravelPlan(
            id = uuid4(),
            title="Foo",
            location_name="Praha",
            location_lat=49,
            location_long=16,
            arrival_date=datetime(2024, 1, 31),
            departure_date=datetime(2024, 2, 1),
            user_email="bar@example.com"
        ),
    ])