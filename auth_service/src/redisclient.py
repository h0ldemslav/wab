import redis
import json

class RedisClient:
    def __init__(self, host='localhost', port=6379):
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

    def get_unique_key(self, email: str):
        return f"user:{email}"

    def set_token(self, email: str, token_data: dict):
        key = self.get_unique_key(email)
        json_object = json.dumps(token_data)

        self.redis_client.set(key, json_object)

    def get_token(self, email: str) -> dict:
        key = self.get_unique_key(email)
        token_data = self.redis_client.get(key)

        return json.loads(token_data)

    def delete_token(self, email: str):
        key = self.get_unique_key(email)
        self.redis_client.delete(key)
    
    def exists(self, email: str) -> bool:
        key = self.get_unique_key(email)
        
        return self.redis_client.exists(key)
