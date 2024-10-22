# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from settings import settings
from firebase import firebase

firebase_session = firebase.FirebaseApplication(settings.database_name, None)


# SQLALCHEMY_DATABASE_URL = f"sqlite:///./{settings.database_name}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
