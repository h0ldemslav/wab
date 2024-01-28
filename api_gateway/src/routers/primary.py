import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import get_google_token_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

api_gateway_routes = {
    "base": "/",
    "home": "/home",
    "logout": "/logout"
}
auth_service_urls = {
    "login": "http://127.0.0.1:8001/login",
    "delete_token": "http://127.0.0.1:8001/delete_token"
}
cookies_keys = {
    "google_token": "google_token"
}

@router.get(api_gateway_routes["base"])
async def root(request: Request):
    google_token = get_google_token_from_cookie(request)

    if google_token:
        return RedirectResponse(url=api_gateway_routes["home"])

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={ "path": auth_service_urls["login"] }
    )

@router.get(api_gateway_routes["home"])
async def home(request: Request):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        return RedirectResponse(url=api_gateway_routes["base"])

    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )

@router.get(api_gateway_routes["logout"])
async def logout(request: Request):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        return RedirectResponse(url=api_gateway_routes["base"])

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(auth_service_urls["delete_token"], json=google_token.dict())
        except Exception:
            raise HTTPException(status_code=500, detail="Fail to logout")
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.content.decode("utf-8"))

        redirect = RedirectResponse(url=api_gateway_routes["base"])
        redirect.delete_cookie(cookies_keys.get("google_token", ""))

        return redirect