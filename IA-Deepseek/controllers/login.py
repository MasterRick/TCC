# main.py
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session
from db import get_db
from auth.auth import create_access_token
from services import user as user_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_service.login_user_service(form_data, db)
