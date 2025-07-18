from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DescriptorOut (BaseModel):
    id: int
    name: str
    content: str
    year: str
    classroom: str
    discipline: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
    