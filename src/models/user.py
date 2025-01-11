from sqlalchemy import Column, String
from db import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
