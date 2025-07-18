from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.auth import create_access_token
from models.user import User
from bodies.user import UserCreate, UserLogin, UserOut
from fastapi import Depends, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def login_user_service(user: OAuth2PasswordRequestForm, db: Session) -> dict:
    db_user = db.query(User).filter(User.email == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
    
    

def create_user_service(user: UserCreate, db: Session) -> User:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
