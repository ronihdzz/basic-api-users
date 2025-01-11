import init_import
from src.db import engine
from src.models.user import User
import logging
from loguru import logger


tables_to_create = [
    User.__table__
]

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

for table in tables_to_create:
    logger.info(f"Intentando crear la tabla {table.name} si no existe...")
    table.create(bind=engine, checkfirst=True)
    logger.info(f"Tabla {table.name} verificada/creada exitosamente.")

logger.info("Proceso de creación/verificación de tablas finalizado.")