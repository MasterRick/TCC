
import os
import time
import asyncio
from collections import defaultdict, deque
from pathlib import Path

from dotenv import load_dotenv

from db import Base, engine
from models import user, descriptor, rating, question, type
from fastapi import FastAPI, Request
from controllers import user as user_router, login as login_router, rating as rating_router, question as question_router, descriptor as descriptor_router, exam as exam_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse


Base.metadata.create_all(bind=engine)
app = FastAPI()

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
RATE_LIMIT = int(os.getenv("RATE_LIMIT"))  # Requisições por minuto
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS"))  # Tempo limite para respostas
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS"))  # Janela de tempo para o rate limit

request_history: dict[str, deque[float]] = defaultdict(deque)
request_history_lock = asyncio.Lock()


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    if TIMEOUT_SECONDS <= 0:
        return await call_next(request)

    try:
        return await asyncio.wait_for(call_next(request), timeout=TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"detail": f"Request timeout after {TIMEOUT_SECONDS} seconds"},
        )


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if RATE_LIMIT <= 0:
        return await call_next(request)

    client_ip = get_client_ip(request)
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    async with request_history_lock:
        history = request_history[client_ip]

        while history and history[0] < window_start:
            history.popleft()

        if len(history) >= RATE_LIMIT:
            retry_after = int(max(1, RATE_LIMIT_WINDOW_SECONDS - (now - history[0])))
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."},
                headers={"Retry-After": str(retry_after)},
            )

        history.append(now)

    return await call_next(request)


app.include_router(user_router.router)
app.include_router(login_router.router)
app.include_router(rating_router.router)
app.include_router(question_router.router)
app.include_router(descriptor_router.router)
app.include_router(exam_router.router)