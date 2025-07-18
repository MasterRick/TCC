
from db import Base, engine
from models import user, descriptor, rating, question
from fastapi import FastAPI
from controllers import user as user_router, login as login_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user_router.router)
app.include_router(login_router.router)

   
        
        
        