
import datetime
from typing import Optional
from pydantic import BaseModel
from bodies.descriptor import DescriptorOut

class QuestionOut(BaseModel):
    id: int
    difficulty: int
    content: dict[str, str]
    rating: Optional[float] = None
    descriptor: DescriptorOut   
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    difficulty: int
    content: str
    descriptor_id: int

class QuestionByFileCreate(BaseModel):
    difficulty: int
    discipline: str
    classroom: str
    year: str
    content: str