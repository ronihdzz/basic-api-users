from db import context_get_db
from sqlalchemy import select, or_
from models import User
from uuid import UUID
class UserRepository:
    
    @classmethod
    def get_user_by_name_or_email(cls, username: str, email: str)-> User | None:
        query = select(User).where(
            or_(User.username == username, User.email == email)
        )
        with context_get_db() as session:
            return session.execute(query).scalars().first()
    
    @classmethod
    def get_user_by_name(cls, username: str)-> User | None:
        query = select(User).where(
            User.username == username
        )
        with context_get_db() as session:
            return session.execute(query).scalars().first()
    
    @classmethod
    def get_user_by_id(cls, user_id: UUID)-> User | None:
        query = select(User).where(
            User.id == user_id
        )
        with context_get_db() as session:
            return session.execute(query).scalars().first()
    
    @classmethod
    def create_user(cls, user: User)-> User:
        with context_get_db() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    @classmethod
    def delete_user(cls, user: User)-> None:
        with context_get_db() as session:
            session.delete(user)
            session.commit()
