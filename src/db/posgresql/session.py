from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from sqlalchemy.pool import NullPool

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"application_name": settings.PROJECT_NAME},
    poolclass=NullPool
)
SessionLocal = sessionmaker(autocommit=False, bind=engine)


@contextmanager
def context_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()