from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from bodies.user import UserCreate, UserOut
from services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user_service(user, db)
