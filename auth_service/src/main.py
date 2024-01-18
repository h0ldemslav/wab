from fastapi import FastAPI

app = FastAPI()
itinerary_service_url = "http://127.0.0.1:8000" 

@app.get("/login")
async def root():
    return {"login": "Logging in..."}