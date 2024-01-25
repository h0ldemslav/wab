import httpx
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
api_gateway_routes = {
    "base": "/",
    "home": "/home",
    "logout": "/logout"
}
auth_service_urls = {
    "base": "http://127.0.0.1:8001",
    "login": "http://127.0.0.1:8001/login",
    "delete_token": "http://127.0.0.1:8001/delete_token"
}
cookies_keys = {
    "google_token": "google_token"
}

@app.get(api_gateway_routes["base"])
async def root(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    
    if google_token_json:
        return RedirectResponse(url=api_gateway_routes["home"])

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"path": auth_service_urls["login"]}
    )

@app.get(api_gateway_routes["home"])
async def home(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])

    if not google_token_json:
        return RedirectResponse(url=api_gateway_routes["base"])

    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )

@app.get(api_gateway_routes["logout"])
async def logout(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])

    if not google_token_json:
        raise HTTPException(status_code=400, detail="Fail to logout: invalid cookie")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(auth_service_urls["delete_token"], content=google_token_json)
        except Exception:
            raise HTTPException(status_code=500, detail="Fail to logout")
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.content.decode("utf-8"))

        redirect = RedirectResponse(url=api_gateway_routes["base"])
        redirect.delete_cookie(cookies_keys["google_token"])

        return redirect