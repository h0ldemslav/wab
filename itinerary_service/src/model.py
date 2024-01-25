from typing import List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserInfo(BaseModel):
    email: str
    name: str
    iat: int
    exp: int

class Token(BaseModel):
    access_token: str
    token_type: str
    id_token: str
    expires_at: int
    userinfo: UserInfo

class TravelPlan (BaseModel):
    id: UUID
    title: str
    location_name: str
    location_lat: float
    location_long: float
    arrival_date: datetime
    departure_date: datetime
    user_email: str

class TravelPlanResponse (BaseModel):
    data: List[TravelPlan]