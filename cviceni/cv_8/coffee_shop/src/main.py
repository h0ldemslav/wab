import grpc
import rating_pb2_grpc
import rating_pb2
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/coffee-shop/{id}")
def get_coffee_shop(id: str):
    # pripojim se ke kanalu, ktery jsem nadefinoval
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = rating_pb2_grpc.RatingServiceStub(channel)
        
        # Provolam a poslu pozadavek
        response = stub.lastRating(rating_pb2.LastRatingRequest(coffee_shop_id=id, amount=3))
        
        # Vratim odpoved 
        return response