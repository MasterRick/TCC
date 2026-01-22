from typing import Optional
from fastapi import HTTPException, Query
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from bodies.exam import ExamCreate
from db import get_db
from services import exam as exam_service

router = APIRouter(prefix="/exam", tags=["exam"])

@router.post("")
def start_exam(
    created_exam: ExamCreate,
    db: Session = Depends(get_db),
    current_user: dict[str, int] = Depends(get_current_user)
):
    try:
        return exam_service.create_exam_service(db, current_user, created_exam)
    except HTTPException as e:
        raise e