from settings import settings, DatabaseType
from loguru import logger

if settings.DATABASE_TYPE == DatabaseType.POSTGRESQL:
    from .posgresql import BaseModel, get_db, Base, engine, context_get_db
    logger.info("Using PostgreSQL database")
elif settings.DATABASE_TYPE == DatabaseType.SQLITE:
    from .sqlalchemy import BaseModel, get_db, Base, engine, context_get_db
    logger.info("Using SQLite database")
else:
    raise ValueError(f"Invalid database type: {settings.DATABASE_TYPE}, must be one of {DatabaseType.POSTGRESQL, DatabaseType.SQLITE}")

__all__ = ["BaseModel", "get_db", "Base", "engine", "context_get_db"]