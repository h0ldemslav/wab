from fastapi import FastAPI, Request
from auth import setup_auth

app = FastAPI()

oauth = setup_auth(app)
api_gateway_url = "http://127.0.0.1:8000"

@app.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, "http://127.0.0.1:8001/token")

@app.get("/token")
async def token(request: Request):
    access_token = await oauth.google.authorize_access_token(request)

    return access_token