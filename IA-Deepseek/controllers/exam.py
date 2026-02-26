from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from bodies.exam import ExamCreate
from bodies.question import QuestionOut
from db import get_db
from services import exam as exam_service

router = APIRouter(prefix="/exam", tags=["exam"])

@router.get("/questions/{difficulty}/{discipline}/{classroom}/{year}", response_model=list[QuestionOut])
def get_questions_for_exam(
    difficulty: int,
    discipline: str,
    classroom: str,
    year: str,
    db: Session = Depends(get_db),
    current_user: dict[str, int] = Depends(get_current_user)
):
    try:
        return exam_service.get_questions(db, current_user, difficulty, discipline, classroom, year)
    except HTTPException as e:
        raise e