import os
import grpc
import time
from pathlib import Path
from dotenv import load_dotenv
from concurrent import futures
from grpc_output.itinerary_pb2_grpc import add_ItineraryServiceServicer_to_server
from dbclient import DbClient
from grpcserver import ItineraryServiceServicerImpl

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

db_client = DbClient(user=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"))

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ItineraryServiceServicer_to_server(ItineraryServiceServicerImpl(db_client=db_client), server)

    server.add_insecure_port('localhost:50051')
    server.start()
    
    print("[GRPC Server]: Started listening")

    # Only for development
    time.sleep(600_000)

if __name__ == "__main__":
    serve_grpc()