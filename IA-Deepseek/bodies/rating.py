from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from bodies.user import UserOut
from bodies.question import QuestionOut

class RatingBase(BaseModel):
    question: int
    score: int

class RatingCreate(RatingBase):
    pass


class RatingOut(BaseModel):
    id: int
    user: UserOut
    question: QuestionOut
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True