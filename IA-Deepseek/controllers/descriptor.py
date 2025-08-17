import fastapi
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from db import get_db
from bodies.descriptor import DescriptorOut
from services import descriptor as descriptor_service

router = APIRouter(prefix="/descriptors", tags=["descriptors"])

@router.get("", response_model=list[DescriptorOut],)
def get_descriptors(db: Session = Depends(get_db), 
                    current_user: dict[str, int] = Depends(get_current_user), 
                    page: int = Query(1, ge=1)):
    
    return descriptor_service.get_descriptors_service(page=page, db=db)
