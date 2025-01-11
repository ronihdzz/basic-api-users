from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    @declared_attr
    def id(cls):
        return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)