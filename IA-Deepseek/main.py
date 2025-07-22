
from db import Base, engine
from models import user, descriptor, rating, question
from fastapi import FastAPI
from controllers import user as user_router, login as login_router, rating as rating_router, question as question_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router.router)
app.include_router(login_router.router)
app.include_router(rating_router.router)
app.include_router(question_router.router)

   
        
        
        