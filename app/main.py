from typing import List
import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from . import schemas, database, crud

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def api_create_user(user: schemas.UserCreate, db=Depends(database.get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=List[schemas.User])
def api_read_users(skip: int = 0, limit: int = 10, db=Depends(database.get_db)):
    return crud.get_users(db, skip, limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def api_read_user(user_id: int, db=Depends(database.get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def api_update_user(user_id: int, user: schemas.UserCreate, db=Depends(database.get_db)):
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def api_delete_user(user_id: int, db=Depends(database.get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def api_create_post_for_user(user_id: int, post: schemas.PostCreate, db=Depends(database.get_db)):
    post = crud.create_post(db, post, user_id)
    return post

@app.get("/posts/", response_model=List[schemas.Post])
def api_read_posts(skip: int = 0, limit: int = 10, db=Depends(database.get_db)):
    return crud.get_posts(db, skip, limit)

@app.get("/posts/{post_id}", response_model=schemas.Post)
def api_read_post(post_id: int, db=Depends(database.get_db)):
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=schemas.Post)
def api_update_post(post_id: int, post: schemas.PostCreate, db=Depends(database.get_db)):
    updated_post = crud.update_post(db, post_id, post)

    return updated_post

@app.delete("/posts/{post_id}", response_model=schemas.Post)
def api_delete_post(post_id: int, db=Depends(database.get_db)):
    deleted_post = crud.delete_post(db, post_id)
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return deleted_post

@app.get("/users/{user_id}/posts/", response_model=List[schemas.Post])
def api_read_posts_by_user(user_id: int, db=Depends(database.get_db)):
    return crud.get_posts_by_user(db, user_id)
