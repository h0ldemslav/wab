from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PostReview(BaseModel):
    rating: int
    description: str | None = None
    coffee_shop_id: UUID
    user_id: UUID

class Review(PostReview):
    id: UUID
    created_at: datetime