from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from sqlalchemy.pool import NullPool
from shared.path import BASE_DIR

DATABASE_URL = f"sqlite:///{BASE_DIR}/{settings.DATABASE_URL}.sqlite"
print(DATABASE_URL)
engine = create_engine(
    DATABASE_URL, 
    poolclass=NullPool
)
SessionLocal = sessionmaker(autocommit=False, bind=engine)


# TODO: Decidir si se va a usar o no
# @contextmanager
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()