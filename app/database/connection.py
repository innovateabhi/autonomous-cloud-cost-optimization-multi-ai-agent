from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD
)


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME
)


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
