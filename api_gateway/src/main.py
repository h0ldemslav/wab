import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from model import TravelPlanResponse, Token

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
api_gateway_routes = {
    "base": "/",
    "home": "/home",
    "logout": "/logout",
    "travel_plans": "/travel_plans"
}
auth_service_urls = {
    "base": "http://127.0.0.1:8001",
    "login": "http://127.0.0.1:8001/login",
    "delete_token": "http://127.0.0.1:8001/delete_token"
}
itinerary_service_urls = {
    "travel_plans": "http://127.0.0.1:8002/travel_plans"
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

@app.get(api_gateway_routes["travel_plans"])
async def get_travel_plans(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])

    validate_token_schema(google_token_json)

    async with httpx.AsyncClient() as client:
        response = await client.post(itinerary_service_urls["travel_plans"], content=google_token_json)
        travel_plan_response = convert_json_to_travel_plan_response(response.content)
        
        return templates.TemplateResponse(
            request=request,
            name="travel_plans.html",
            context={ "travel_plans": travel_plan_response.data }
        )

def convert_json_to_travel_plan_response(json: str) -> TravelPlanResponse:
    try:
        return TravelPlanResponse.model_validate_json(json)
    except ValueError:
        raise HTTPException(status_code=500, detail="Fail to convert data")

def validate_token_schema(tokenJson: str) -> Token:
    try:
        return Token.model_validate_json(tokenJson)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token")