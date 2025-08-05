from sqlalchemy.orm import Session
from models.descriptor import Descriptor
from models.question import Question

PAGE_SIZE = 50

def get_descriptors_service (page: int = 1,  db: Session = None):
    offset = (page - 1) * PAGE_SIZE
    descriptors = db.query(Descriptor).offset(offset).limit(PAGE_SIZE).all()
    return descriptors
