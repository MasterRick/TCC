import datetime as dt
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)

    question = relationship("Question", backref="ratings")
    user = relationship("User", backref="ratings")

    created_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Rating(id={self.id}, question_id={self.question_id}, user_id={self.user_id}, score={self.score})>"
