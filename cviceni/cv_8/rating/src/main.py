import grpc
from concurrent import futures
import rating_pb2_grpc as rating_pb2_grpc
import time

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # na kolika vlaknech muze pracovat (definuje futures)
    rating_pb2_grpc.add_RatingServiceServicer_to_server(rating_pb2_grpc.RatingServiceServicer, server) # propojeni kodu se servisem
    server.add_insecure_port("[::]:5001")
    server.start()
    time.sleep(600_000)
    # jsem na serveru a jdeme do klienta

if __name__ == "__main__":
    serve()