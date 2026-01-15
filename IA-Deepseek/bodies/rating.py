from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from bodies.user import UserOut
from bodies.question import QuestionOut

class RatingBase(BaseModel):
    question: int
    coherence: float
    contextualization: float
    difficulty_level: float
    clarity: float
    descriptor_alignment: float
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    pass


class RatingOut(BaseModel):
    id: int
    question_id: int
    user_id: int
    coherence: float
    contextualization: float
    difficulty_level: float
    clarity: float
    descriptor_alignment: float
    comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True