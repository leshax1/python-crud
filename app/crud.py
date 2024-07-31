
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from . import schemas
from psycopg2.errors import UniqueViolation
from fastapi import HTTPException

def get_user(conn, user_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()

def get_users(conn, skip: int = 0, limit: int = 10):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users LIMIT %s OFFSET %s", (limit, skip))
        return cur.fetchall()

def create_user(conn, user: schemas.UserCreate):
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *", (user.name, user.email))
            conn.commit()
            return cur.fetchone()
    except UniqueViolation as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Email {user.email} already exists.")

def update_user(conn, user_id: int, user: schemas.UserCreate):
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING *", (user.name, user.email, user_id))
        updated_user = cur.fetchone()
        
        if updated_user:
            conn.commit()
            return updated_user
        else:
            cur.execute(
                "INSERT INTO users (id, name, email) VALUES (%s, %s, %s) RETURNING *",
                (user_id, user.name, user.email)
            )
            new_user = cur.fetchone()
            conn.commit()
            return new_user

def delete_user(conn, user_id: int):
   with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (user_id,))
        deleted_user = cur.fetchone()
        conn.commit()
        return deleted_user

def get_post(conn, post_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        return cur.fetchone()

def get_posts(conn, skip: int = 0, limit: int = 10):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts LIMIT %s OFFSET %s", (limit, skip))
        return cur.fetchall()

def create_post(conn, post: schemas.PostCreate, user_id: int):
    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO posts (title, content, owner_id) VALUES (%s, %s, %s) RETURNING *",
                (post.title, post.content, user_id)
            )
            conn.commit()
            return cur.fetchone()
        except Exception as e:
            conn.rollback()
            return None

def update_post(conn, post_id: int, post: schemas.PostCreate):
     with conn.cursor() as cur:
        cur.execute(
            "UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *",
            (post.title, post.content, post_id)
        )
        updated_post = cur.fetchone()
        conn.commit()
        
        return updated_post

def delete_post(conn, post_id: int):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
        conn.commit()
        return cur.fetchone()

def get_posts_by_user(conn, user_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts WHERE owner_id = %s", (user_id,))
        return cur.fetchall()
