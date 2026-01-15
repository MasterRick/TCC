import datetime as dt
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)

    question = relationship("Question", backref="ratings")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    user = relationship("User", backref="ratings")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Critérios de avaliação
    coherence = Column(Float, nullable=False, default=0)  # Coerência dos enunciados
    contextualization = Column(Float, nullable=False, default=0)  # Contextualização adequada
    difficulty_level = Column(Float, nullable=False, default=0)  # Nível de dificuldade apropriado
    clarity = Column(Float, nullable=False, default=0)  # Clareza das alternativas
    descriptor_alignment = Column(Float, nullable=False, default=0)  # Alinhamento com descritor
    
    comment = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Rating(id={self.id}, question_id={self.question_id}, user_id={self.user_id})>"
