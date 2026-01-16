from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from db import get_db
from bodies.question import QuestionCreate, QuestionOut
from services import question as question_service
from fastapi import HTTPException

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("", response_model=list[QuestionOut])
def get_questions(
    db: Session = Depends(get_db),
    current_user: dict[str, int] = Depends(get_current_user),
    page: int = Query(1, ge=1),
    descriptor_id: Optional[int] = Query(None, ge=1),
    difficulty: Optional[int] = Query(None, ge=0),
    discipline: Optional[str] = Query(None, min_length=1, max_length=3),
    classroom: Optional[str] = Query(None, min_length=1, max_length=3),
    year: Optional[str] = Query(None, min_length=4, max_length=6)
):
    try:
        return question_service.get_questions_service(db, current_user.get("id"), page, descriptor_id, difficulty, discipline, classroom, year)
    except HTTPException as e:
        raise e

@router.get("/create-status")
def process_status(db: Session = Depends(get_db), 
                   current_user: dict[str, int] = Depends(get_current_user), 
                   ):

    return question_service.get_process_status()

@router.get("/{question_id}", response_model=QuestionOut)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: dict[str, int] = Depends(get_current_user)
):
    try:
        return question_service.get_question_service(question_id, db)
    except HTTPException as e:
        raise e

@router.post("/create", response_model=dict[str, str])
def create_questions(background_tasks: BackgroundTasks,
                     db: Session = Depends(get_db), 
                     current_user: dict[str, int] = Depends(get_current_user),
                     ):

    return question_service.create_questions_service(db=db, current_user=current_user, background_tasks=background_tasks)

@router.post("/create-single", response_model=dict[str, str])
def create_single_question(
    background_tasks: BackgroundTasks,
    question_info:QuestionCreate,
    ):

    try:
        return question_service.create_questions_service_single(question_info, background_tasks)
    except HTTPException as e:
        raise e
