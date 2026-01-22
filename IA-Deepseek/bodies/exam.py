
from pydantic import BaseModel

class ExamOut (BaseModel):
    id: int
    difficulty: int
    discipline: str 
    classroom: str
    year: str
    questions: list[int]

    class Config:
        from_attributes = True

class ExamCreate (BaseModel):
    difficulty: int
    discipline: str 
    classroom: str
    year: str
    questions: list[int] = None