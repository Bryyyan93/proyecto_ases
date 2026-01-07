from sqlalchemy import create_engine
from app.config.settings import DATABASE_URL
import os


DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('DOMINIO')}:"
    f"{os.getenv('PUERTO_DOMINIO')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)
