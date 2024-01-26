import grpc
import httpx
from typing import Annotated
from starlette import status
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from grpc_output.itinerary_pb2 import Token, UserInfo, TokenWithTravelPlan, TravelPlan
from grpc_output.itinerary_pb2_grpc import ItineraryServiceStub
from models import GoogleToken

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
api_gateway_routes = {
    "base": "/",
    "home": "/home",
    "logout": "/logout",
    "travel_plans": "/travel_plans",
    "create_travel_plan": "/create_travel_plan"
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
    google_token = get_google_token_from_json(google_token_json)
    
    if google_token:
        return RedirectResponse(url=api_gateway_routes["home"])

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={ "path": auth_service_urls["login"] }
    )

@app.get(api_gateway_routes["home"])
async def home(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=api_gateway_routes["base"])

    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )

@app.get(api_gateway_routes["logout"])
async def logout(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        raise HTTPException(status_code=400, detail="Fail to logout: invalid cookie")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(auth_service_urls["delete_token"], json=google_token.dict())
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
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=api_gateway_routes["base"])

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)

        try:
            response = stub.GetTravelPlans(
                Token(
                    access_token=google_token.access_token,
                    token_type=google_token.token_type,
                    id_token=google_token.id_token,
                    expires_at=google_token.expires_at,
                    userinfo=UserInfo(
                        email=google_token.userinfo.email, 
                        name=google_token.userinfo.name
                    )
                )
            )
            
            return templates.TemplateResponse(
                request=request, 
                name="travel_plans.html",
                context={ "travel_plans": response.data }
            )
        except grpc.RpcError:
            raise HTTPException(status_code=401)

@app.get(api_gateway_routes["create_travel_plan"])
def create_travel_plan(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=api_gateway_routes["base"])
    
    return templates.TemplateResponse(
        request=request, 
        name="create_travel_plan.html"
    )

@app.post(api_gateway_routes["create_travel_plan"])
async def create_travel_plan(
    request: Request,
    title: Annotated[str, Form()], 
    desc: Annotated[str, Form()]
):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=api_gateway_routes["base"]) 

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)
        travel_plan = TravelPlan(
            id="",
            title=title,
            description=desc,
            user_email=google_token.userinfo.email
        )
        token = Token(
            access_token=google_token.access_token,
            token_type=google_token.token_type,
            id_token=google_token.id_token,
            expires_at=google_token.expires_at,
            userinfo=UserInfo(
                email=google_token.userinfo.email, 
                name=google_token.userinfo.name
            )
        )

        try:
            stub.CreateTravelPlan(TokenWithTravelPlan(
                token=token, 
                travel_plan=travel_plan
            ))
            
            return RedirectResponse(
                url=api_gateway_routes["travel_plans"], 
                # Workaround to redirect with GET method
                status_code=status.HTTP_302_FOUND
            )
        except grpc.RpcError:
            raise HTTPException(status_code=401)

def get_google_token_from_json(json: str) -> GoogleToken | None:
    try:
        return GoogleToken.model_validate_json(json)
    except ValueError:
        return None