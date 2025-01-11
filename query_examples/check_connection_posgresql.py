import init_import 
import psycopg2
from src.settings import settings
from loguru import logger

def test_connection():
    connection = None
    try:
        connection_url = settings.DATABASE_URL
        logger.info(f"Connection URL: {connection_url}")
        
        logger.info(f"Starting connection to database")
        connection = psycopg2.connect(connection_url)
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        logger.info(f"Connection successful. Database version: {db_version}")
        
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error connecting to database: {error}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("Connection closed.")
        else:
            logger.info("No connection created")

if __name__ == "__main__":
    test_connection()