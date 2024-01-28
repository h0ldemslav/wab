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
            grpc_travel_plan = self.convert_db_travel_plan_to_grpc(item)
            grpc_travel_plans.append(grpc_travel_plan)

        return itinerary_pb2.TravelPlanResponse(data=grpc_travel_plans)
    
    def GetTravelPlanById(self, request, context):
        self.validate_token(request.token, context)

        db_travel_plan: schemas.TravelPlan = self.db_client.get_travel_plan_by_id(request.travelPlanId)
        grpc_travel_plan = self.convert_db_travel_plan_to_grpc(db_travel_plan)

        return grpc_travel_plan
    
    def CreateTravelPlan(self, request, context):
        self.validate_token(request.token, context)

        grpc_travel_plan: itinerary_pb2.TravelPlan = request.travel_plan
        
        self.db_client.create_new_travel_plan(schemas.TravelPlan(
            title=grpc_travel_plan.title,
            description=grpc_travel_plan.description,
            user_email=grpc_travel_plan.user_email
        ))

        return grpc_travel_plan

    def DeleteTravelPlanById(self, request, context):
        self.validate_token(request.token, context)
        self.db_client.delete_travel_plan_by_id(request.travelPlanId)

        return itinerary_pb2.Empty()

    def UpdateTravelPlanById(self, request, context):
        self.validate_token(request.token, context)
        db_travel_plan: schemas.TravelPlan = self.convert_grpc_to_db_travel_plan(request.travel_plan)
        self.db_client.update_travel_plan(db_travel_plan)

        return request.travel_plan

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
    
    def convert_db_travel_plan_to_grpc(self, travel_plan: schemas.TravelPlan) -> itinerary_pb2.TravelPlan:
        return itinerary_pb2.TravelPlan(
            id=travel_plan.id,
            title=travel_plan.title,
            description=travel_plan.description,
            location_name=travel_plan.location_name,
            location_lat=travel_plan.location_lat,
            location_long=travel_plan.location_long,
            arrival_date=travel_plan.arrival_date,
            departure_date=travel_plan.departure_date,
            user_email=travel_plan.user_email
        )
    
    def convert_grpc_to_db_travel_plan(self, travel_plan: itinerary_pb2.TravelPlan):
        return schemas.TravelPlan(
            id=travel_plan.id,
            title=travel_plan.title,
            description=travel_plan.description,
            location_name=travel_plan.location_name,
            location_lat=travel_plan.location_lat,
            location_long=travel_plan.location_long,
            arrival_date=travel_plan.arrival_date,
            departure_date=travel_plan.departure_date,
            user_email=travel_plan.user_email
        )