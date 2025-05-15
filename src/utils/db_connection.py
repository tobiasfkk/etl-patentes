import time
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    retries = int(os.getenv("DB_CONNECTION_RETRIES", 10))  # Configurável via env
    while retries > 0:
        try:
            print("Attempting to connect to the database...")
            return psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "patents_db"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                cursor_factory=RealDictCursor
            )
        except psycopg2.OperationalError as e:
            print(f"Database is not ready: {e}, retrying in 5 seconds...")
            retries -= 1
            time.sleep(5)
    raise Exception("Failed to connect to the database after multiple retries.")