from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from auth import setup_auth

app = FastAPI()

oauth = setup_auth(app)
oauth_data = {}
api_gateway_url = "http://127.0.0.1:8000"

@app.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, "http://127.0.0.1:8001/token")

@app.get("/token")
async def token(request: Request):
    try:
        oauth_data["token"] = await oauth.google.authorize_access_token(request)
        redirect_url = f"{api_gateway_url}/home"

        return RedirectResponse(url=redirect_url)
    except Exception:
        return RedirectResponse(url=api_gateway_url)