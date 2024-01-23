import json
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from auth import setup_auth
from redisclient import RedisClient

app = FastAPI()
redis_client = RedisClient()

oauth = setup_auth(app)
oauth_data = {}
auth_service_routes = {
    "base": "http://127.0.0.1:8001",
    "login": "http://127.0.0.1:8001/login",
    "token": "http://127.0.0.1:8001/token"
}
api_gateway_routes = {
    "base": "http://127.0.0.1:8000",
    "home": "http://127.0.0.1:8000/home"
}

@app.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, auth_service_routes["token"])

@app.get(
    path="/token",
    include_in_schema=False
)
async def token(request: Request):
    try:
        token_data = await oauth.google.authorize_access_token(request)
        user_email = token_data["userinfo"]["email"]

        redis_client.set_token(user_email, token_data)

        response = RedirectResponse(url=api_gateway_routes["home"])
        response.set_cookie(key="google_token", value=json.dumps(token_data), secure=True, httponly=True)

        return response
    except Exception:
        return RedirectResponse(url=api_gateway_routes["base"])

@app.post("/delete_token")
async def logout(request: Request):
    user_email = await request.body()

    if not user_email:
        return RedirectResponse(url=api_gateway_routes["base"]) 

    redis_client.delete_token(user_email)