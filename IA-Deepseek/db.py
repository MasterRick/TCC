import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

senha_codificada = quote_plus(DB_PASSWORD)

DATABASE_URL = f"mysql+pymysql://admin:{senha_codificada}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=30,           # Número máximo de conexões no pool
    max_overflow=30,        # Número máximo de conexões extras acima do pool_size
    pool_timeout=120,        # Tempo máximo (segundos) para esperar por uma conexão
    connect_args={"connect_timeout": 120}  # Timeout de conexão ao MySQL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()