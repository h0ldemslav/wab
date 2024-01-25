import grpc
import time
import httpx
from uuid import uuid4
from datetime import datetime
from concurrent import futures
from grpc_output.itinerary_pb2 import TravelPlanResponse, TravelPlan
from grpc_output.itinerary_pb2_grpc import ItineraryServiceServicer, add_ItineraryServiceServicer_to_server

class ItineraryServiceServicerImpl(ItineraryServiceServicer):
    def GetTravelPlans(self, request, context):
        auth_service_url = "http://127.0.0.1:8001/validate_token"
        response = httpx.post(auth_service_url, content=request.token)

        if response.status_code != 200:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        # TODO: replace with db
        travel_plan = TravelPlan(
            id=str(uuid4()),
            title="Foo",
            location_name="Praha",
            location_lat=49,
            location_long=16,
            arrival_date=int(datetime(2024, 1, 31).timestamp()),
            departure_date=int(datetime(2024, 2, 1).timestamp()),
            user_email="bar@example.com"
        )

        return TravelPlanResponse(data=[travel_plan])

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