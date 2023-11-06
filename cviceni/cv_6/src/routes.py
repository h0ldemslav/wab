from fastapi import APIRouter
from .schemas import *

router = APIRouter()

@router.get("/review")
async def get_reviews() -> list[Review]:
    # nevracej None, jinak dostanes 500
    return [
        
    ]

@router.post("/review", status_code=201)
async def post_review(post_review_body: PostReview) -> Review:
    pass