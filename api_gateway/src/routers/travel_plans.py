import grpc
from grpc_output.itinerary_pb2 import Token, UserInfo, TokenWithTravelPlan, TravelPlan
from grpc_output.itinerary_pb2_grpc import ItineraryServiceStub
from typing import Annotated
from starlette import status
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import get_google_token_from_json

router_prefix = "/travel_plans"
router = APIRouter(prefix=router_prefix)
templates = Jinja2Templates(directory="src/templates")

routes = {
    "base": "/",
    "new": "/new",
    "login": "http://127.0.0.1:8000"
}
cookies_keys = {
    "google_token": "google_token"
}

@router.get(routes["base"])
async def get_travel_plans(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=routes["login"])

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

@router.get(routes["new"])
def create_travel_plan(request: Request):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=routes["login"])
    
    return templates.TemplateResponse(
        request=request, 
        name="create_travel_plan.html"
    )

@router.post(routes["new"])
async def create_travel_plan(
    request: Request,
    title: Annotated[str, Form()], 
    desc: Annotated[str, Form()]
):
    google_token_json = request.cookies.get(cookies_keys["google_token"])
    google_token = get_google_token_from_json(google_token_json)

    if not google_token:
        return RedirectResponse(url=routes["login"]) 

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)
        travel_plan = TravelPlan(
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
                url=f"{ router_prefix }{ routes['base'] }", 
                # Workaround to redirect with GET method
                status_code=status.HTTP_302_FOUND
            )
        except grpc.RpcError:
            raise HTTPException(status_code=401)