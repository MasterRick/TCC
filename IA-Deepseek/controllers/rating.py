from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from db import get_db
from bodies.rating import RatingCreate, RatingOut
from services import rating as rating_service

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/", response_model=RatingOut)
def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: dict[str, int] = Depends(get_current_user)
):
    try:
        return rating_service.create_rating_service(rating, db, current_user)
    except HTTPException as e:
        raise e