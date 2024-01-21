import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from auth import setup_auth

app = FastAPI()

oauth = setup_auth(app)
oauth_data = {}
auth_service_urls = {
    "base": "http://127.0.0.1:8001",
    "login": "http://127.0.0.1:8001/login",
    "token": "http://127.0.0.1:8001/token"
}
api_gateway_urls = {
    "base": "http://127.0.0.1:8000",
    "home": "http://127.0.0.1:8000/home",
    "process_token": "http://127.0.0.1:8000/process_token"
}

@app.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, auth_service_urls["token"])

@app.get(
    path="/token",
    include_in_schema=False
)
async def token(request: Request):
    try:
        token_data = await oauth.google.authorize_access_token(request)
        oauth_data.update(token_data)

        redirect_url = api_gateway_urls["home"]

        await send_token_to_api_gateway(token_data)

        return RedirectResponse(url=redirect_url)
    except Exception:
        return RedirectResponse(url=api_gateway_urls["base"])

async def send_token_to_api_gateway(access_token: str):
    headers = { "Content-Type": "application/json" }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_gateway_urls["process_token"], json=access_token, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to send token to API Gateway")