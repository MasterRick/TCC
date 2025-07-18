import datetime as dt
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    difficulty = Column(Integer, nullable=False)
    content = Column(String(1000), nullable=False)

    descriptor_id = Column(Integer, ForeignKey("descriptors.id"), nullable=False)
    descriptor = relationship("Descriptor", backref="questions")

    created_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))
    deleted_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Question(id={self.id}, descriptor_id={self.descriptor_id}, difficulty={self.difficulty})>"
