import json
import grpc
import models
from grpc_output import itinerary_pb2
from grpc_output.itinerary_pb2_grpc import ItineraryServiceStub
from typing import Annotated
from starlette import status
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from utils import get_google_token_from_cookie

router_prefix = "/travel_plans"
router = APIRouter(prefix=router_prefix)
templates = Jinja2Templates(directory="src/templates")

routes = {
    "base": "/",
    "new": "/new",
    "travel_plan_by_id": "/plan/{id}",
    "login": "http://127.0.0.1:8000"
}

@router.get(routes["base"])
async def get_travel_plans(request: Request):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        raise HTTPException(status_code=401)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)

        try:
            response = stub.GetTravelPlans(
                itinerary_pb2.Token(
                    access_token=google_token.access_token,
                    token_type=google_token.token_type,
                    id_token=google_token.id_token,
                    expires_at=google_token.expires_at,
                    userinfo=itinerary_pb2.UserInfo(
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

@router.get(routes["travel_plan_by_id"])
async def get_travel_plan_by_id(request: Request, id: str):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        raise HTTPException(status_code=401)
    
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)

        try:
            response = stub.GetTravelPlanById(
                itinerary_pb2.TokenWithTravelPlanId(
                    token=itinerary_pb2.Token(
                        access_token=google_token.access_token,
                        token_type=google_token.token_type,
                        id_token=google_token.id_token,
                        expires_at=google_token.expires_at,
                        userinfo=itinerary_pb2.UserInfo(
                            email=google_token.userinfo.email, 
                            name=google_token.userinfo.name
                        )
                    ),
                    travelPlanId=id
                )
            )
            
            return templates.TemplateResponse(
                request=request, 
                name="travel_plan_by_id.html",
                context={ "travel_plan": response }
            )
        except grpc.RpcError:
            raise HTTPException(status_code=401)

@router.delete(routes["travel_plan_by_id"])
async def delete_travel_plan(request: Request, id: str):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        raise HTTPException(status_code=401)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)

        try:
            stub.DeleteTravelPlanById(
                itinerary_pb2.TokenWithTravelPlanId(
                    token=itinerary_pb2.Token(
                        access_token=google_token.access_token,
                        token_type=google_token.token_type,
                        id_token=google_token.id_token,
                        expires_at=google_token.expires_at,
                        userinfo=itinerary_pb2.UserInfo(
                            email=google_token.userinfo.email, 
                            name=google_token.userinfo.name
                        )
                    ),
                    travelPlanId=id
                )
            )
            
            return RedirectResponse(url=routes["base"], status_code=status.HTTP_303_SEE_OTHER)
        except grpc.RpcError:
            raise HTTPException(status_code=401)

@router.put(routes["travel_plan_by_id"])
async def update_travel_plan(request: Request, id: str):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        raise HTTPException(401)

    try:
        travel_plan_dict = await request.json()
        travel_plan: models.TravelPlan = models.TravelPlan.model_validate(travel_plan_dict)
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(400)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)

        try:
            stub.UpdateTravelPlanById(
                itinerary_pb2.TokenWithTravelPlan(
                    token=itinerary_pb2.Token(
                        access_token=google_token.access_token,
                        token_type=google_token.token_type,
                        id_token=google_token.id_token,
                        expires_at=google_token.expires_at,
                        userinfo=itinerary_pb2.UserInfo(
                            email=google_token.userinfo.email, 
                            name=google_token.userinfo.name
                        )
                    ),
                    travel_plan=itinerary_pb2.TravelPlan(
                        id=id,
                        title=travel_plan.title,
                        description=travel_plan.description,
                        location_name=travel_plan.location_name,
                        location_lat=travel_plan.location_lat,
                        location_long=travel_plan.location_long,
                        arrival_date=travel_plan.arrival_date,
                        departure_date=travel_plan.departure_date,
                        user_email=travel_plan.user_email
                    )
                )
            )
        except grpc.RpcError:
            raise HTTPException(status_code=401)

@router.get(routes["new"])
async def create_travel_plan(request: Request):
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        raise HTTPException(status_code=401)
    
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
    google_token = get_google_token_from_cookie(request)

    if not google_token:
        raise HTTPException(status_code=401)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ItineraryServiceStub(channel)
        travel_plan = itinerary_pb2.TravelPlan(
            title=title,
            description=desc,
            user_email=google_token.userinfo.email
        )
        token = itinerary_pb2.Token(
            access_token=google_token.access_token,
            token_type=google_token.token_type,
            id_token=google_token.id_token,
            expires_at=google_token.expires_at,
            userinfo=itinerary_pb2.UserInfo(
                email=google_token.userinfo.email, 
                name=google_token.userinfo.name
            )
        )

        try:
            stub.CreateTravelPlan(itinerary_pb2.TokenWithTravelPlan(
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