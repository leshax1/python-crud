
from typing import List, Optional
from app import schemas
from . import database

def get_user(conn, user_id: int) -> Optional[schemas.User]:
    query = "SELECT * FROM users WHERE id = %s"
    return database.fetch_one(conn, query, (user_id,))

def get_users(conn, skip: int = 0, limit: int = 10) -> List[schemas.User]:
    query = "SELECT * FROM users LIMIT %s OFFSET %s"
    return database.fetch_all(conn, query, (limit, skip))

def create_user(conn, user: schemas.UserCreate) -> schemas.User:
    query = "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *"
    return database.execute_query(conn, query, (user.name, user.email))

def update_user(conn, user_id: int, user: schemas.UserCreate) -> schemas.User:
    query = "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING *"
    updated_user = database.execute_query(conn, query, (user.name, user.email, user_id))
    
    if updated_user:
        return updated_user
    else:
        query = "INSERT INTO users (id, name, email) VALUES (%s, %s, %s) RETURNING *"
        return database.execute_query(conn, query, (user_id, user.name, user.email))

def delete_user(conn, user_id: int) -> Optional[schemas.User]:
    query = "DELETE FROM users WHERE id = %s RETURNING *"
    return database.execute_query(conn, query, (user_id,))

def get_post(conn, post_id: int) -> Optional[schemas.Post]:
    query = "SELECT * FROM posts WHERE id = %s"
    return database.fetch_one(conn, query, (post_id,))

def get_posts(conn, skip: int = 0, limit: int = 10) -> List[schemas.Post]:
    query = "SELECT * FROM posts LIMIT %s OFFSET %s"
    return database.fetch_all(conn, query, (limit, skip))

def create_post(conn, post: schemas.PostCreate, user_id: int) -> schemas.Post:
    query = "INSERT INTO posts (title, content, owner_id) VALUES (%s, %s, %s) RETURNING *"
    return database.execute_query(conn, query, (post.title, post.content, user_id))

def update_post(conn, post_id: int, post: schemas.PostCreate) -> Optional[schemas.Post]:
    query = "UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *"
    return database.execute_query(conn, query, (post.title, post.content, post_id))

def delete_post(conn, post_id: int) -> Optional[schemas.Post]:
    query = "DELETE FROM posts WHERE id = %s RETURNING *"
    return database.execute_query(conn, query, (post_id,))

def get_posts_by_user(conn, user_id: int) -> List[schemas.Post]:
    query = "SELECT * FROM posts WHERE owner_id = %s"
    return database.fetch_all(conn, query, (user_id,))
