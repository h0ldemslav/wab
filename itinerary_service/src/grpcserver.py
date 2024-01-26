import grpc
import httpx
import schemas
from typing import List
from grpc_output import itinerary_pb2
from grpc_output.itinerary_pb2_grpc import ItineraryServiceServicer
from dbclient import DbClient

class ItineraryServiceServicerImpl(ItineraryServiceServicer):
    def __init__(self, db_client: DbClient):
        self.db_client = db_client

    def GetTravelPlans(self, request, context):        
        self.validate_token(token=request, context=context)

        db_travel_plans: List[schemas.TravelPlan] = self.db_client.get_all_travel_plans_by_email(request.userinfo.email)
        grpc_travel_plans: List[itinerary_pb2.TravelPlan] = []

        for item in db_travel_plans:
            grpc_travel_plan = itinerary_pb2.TravelPlan(
                id=item.id,
                title=item.title,
                description=item.description,
                location_name=item.location_name,
                location_lat=item.location_lat,
                location_long=item.location_long,
                arrival_date=item.arrival_date,
                departure_date=item.departure_date,
                user_email=item.user_email
            )

            grpc_travel_plans.append(grpc_travel_plan)

        return itinerary_pb2.TravelPlanResponse(data=grpc_travel_plans)
    
    def CreateTravelPlan(self, request, context):
        self.validate_token(request.token, context)

        grpc_travel_plan: itinerary_pb2.TravelPlan = request.travel_plan
        
        self.db_client.create_new_travel_plan(schemas.TravelPlan(
            title=grpc_travel_plan.title,
            description=grpc_travel_plan.description,
            user_email=grpc_travel_plan.user_email
        ))

        return grpc_travel_plan      

    def validate_token(self, token: itinerary_pb2.Token, context):
        auth_service_url = "http://127.0.0.1:8001/validate_token"
        token = {
            "access_token": token.access_token,
            "token_type": token.token_type,
            "id_token": token.id_token,
            "expires_at": token.expires_at,
            "userinfo": {
                "email": token.userinfo.email,
                "name": token.userinfo.name
            }
        }
        response = httpx.post(auth_service_url, json=token)

        if response.status_code != 200:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")