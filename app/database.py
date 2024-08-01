from fastapi import HTTPException
from typing import Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation, DatabaseError

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"


def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def fetch_one(conn, query: str, params: Tuple) -> Optional[Any]:
    """Fetch a single record from the database."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchone()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def fetch_all(conn, query: str, params: Tuple) -> List[Any]:
    """Fetch all records from the database."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def execute_query(conn, query: str, params: Tuple) -> Optional[Any]:
    """Execute a query and optionally return a record."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            conn.commit()
            return cur.fetchone()
    except UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Unique constraint violation.")
    except DatabaseError as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")