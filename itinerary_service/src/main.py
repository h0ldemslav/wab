import grpc
import time
import httpx
from uuid import uuid4
from concurrent import futures
from grpc_output.itinerary_pb2 import TravelPlanResponse, TravelPlan, Token
from grpc_output.itinerary_pb2_grpc import ItineraryServiceServicer, add_ItineraryServiceServicer_to_server

class ItineraryServiceServicerImpl(ItineraryServiceServicer):
    def GetTravelPlans(self, request, context):        
        validate_token(request, context)

        # TODO: replace with db
        travel_plan = TravelPlan(
            id=str(uuid4()),
            title="Foo",
            description="The most beautiful place!",
            user_email="bar@example.com"
        )

        return TravelPlanResponse(data=[travel_plan])
    
    def CreateTravelPlan(self, request, context):
        validate_token(request.token, context)

        travel_plan: TravelPlan = request.travel_plan
        
        # TODO: save to db
        return travel_plan      

def validate_token(token: Token, context):
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ItineraryServiceServicer_to_server(ItineraryServiceServicerImpl(), server)

    server.add_insecure_port('localhost:50051')
    server.start()
    
    print("Server started")

    # Only for development
    time.sleep(600_000)

if __name__ == "__main__":
    serve()