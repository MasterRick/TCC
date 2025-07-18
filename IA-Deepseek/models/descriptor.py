import datetime as dt
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Descriptor(Base):
    __tablename__ = "descriptors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    year = Column(String(4), nullable=False)
    classroom = Column(String(50), nullable=False)
    discipline = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = Column(DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Descriptor(id={self.id}, name='{self.name}', year='{self.year}', classroom='{self.classroom}', discipline='{self.discipline}')>"