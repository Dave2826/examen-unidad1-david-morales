import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'laboratorio')}:"
    f"{os.getenv('MYSQL_PASSWORD', 'laboratorio')}@"
    f"{os.getenv('MYSQL_HOST', 'mysql')}:3306/"
    f"{os.getenv('MYSQL_DATABASE', 'laboratorio')}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()