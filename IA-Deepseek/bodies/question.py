
import datetime
from typing import Optional
from pydantic import BaseModel
from bodies.descriptor import DescriptorOut

class QuestionOut(BaseModel):
    id: int
    difficulty: int
    content: str
    descriptor: DescriptorOut   
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True