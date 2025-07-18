from fastapi import HTTPException
from sqlalchemy.orm import Session
from bodies.rating import RatingCreate, RatingOut
from controllers import user
from models.question import Question
from models.rating import Rating
from models.user import User


def create_rating_service(rating: RatingCreate, db: Session, current_user: dict[str, int]) -> Rating:
    user = db.query(User).filter(User.id == current_user['id']).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    question = db.query(Question).filter(Question.id == rating.question).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_rating = rating.model_dump()
    print(f"Creating rating for user: {user.id} with data: {db_rating}")
    db_rating["user"] = user
    db_rating["question"] = question
    print(f"Rating data after adding user and question: {db_rating}")
    new_rating = Rating(**db_rating)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating
