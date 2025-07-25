from pydantic import BaseModel, EmailStr
from datetime import datetime

from bodies.type import TypeOut

class UserBase(BaseModel):
    username: str
    email: EmailStr
    type_id: int  # 'student', 'teacher', 'admin'

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(UserBase):
    id: int
    type: TypeOut
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True