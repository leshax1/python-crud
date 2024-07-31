
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()
