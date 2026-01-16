import datetime as dt
from fastapi import HTTPException
import os
from pathlib import Path
from dotenv import load_dotenv
from jose import JWTError, jwt

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict, expires_delta: dt.timedelta = None):
    to_encode = data.copy()
    expire = dt.datetime.now(dt.timezone.utc) + (expires_delta or  dt.timedelta(minutes= float(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload do token: {payload}")
        user_id: int = payload.get("id")
        type: int = payload.get("type")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"id": user_id, "type": type}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
