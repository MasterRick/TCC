import fastapi
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from db import get_db
from bodies.descriptor import DescriptorOut
from services import admin as admin_service

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/create-questions", response_model=dict[str, str])
def create_questions(db: Session = Depends(get_db), 
                     current_user: dict[str, int] = Depends(get_current_user), 
                     ):

    return admin_service.create_questions_service(db=db, current_user=current_user)

@router.get("/create-questions-status")
def process_status(db: Session = Depends(get_db), 
                   current_user: dict[str, int] = Depends(get_current_user), 
                   ):

    return admin_service.get_process_status()