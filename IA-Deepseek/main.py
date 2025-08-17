
from db import Base, engine
from models import user, descriptor, rating, question, type
from fastapi import FastAPI
from controllers import user as user_router, login as login_router, rating as rating_router, question as question_router, descriptor as descriptor_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)
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
app.include_router(descriptor_router.router)
