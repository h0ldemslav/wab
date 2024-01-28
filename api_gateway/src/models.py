from pydantic import BaseModel

class UserInfo(BaseModel):
    email: str
    name: str

class GoogleToken(BaseModel):
    access_token: str
    token_type: str
    id_token: str
    expires_at: int
    userinfo: UserInfo

class TravelPlan(BaseModel):
    id: str
    title: str
    description: str 
    location_name: str | None = None,
    location_lat: float | None = None, 
    location_long: float | None = None, 
    arrival_date: int | None = None,
    departure_date: int | None = None, 
    user_email: str