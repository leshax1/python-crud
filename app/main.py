from fastapi import FastAPI, Depends, HTTPException
from . import schemas, crud, database
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("FastAPI application starting up...")

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate,  db = Depends(database.get_db)):
    return crud.create_user(conn=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db = Depends(database.get_db)):
    return crud.get_users(conn=db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db = Depends(database.get_db)):
    user = crud.get_user(conn=db, user_id=user_id)
    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db = Depends(database.get_db)):
    return crud.update_user(conn=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db = Depends(database.get_db)):
    deleted_user = crud.delete_user(conn=db, user_id=user_id)

    if deleted_user is None: 
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return delete_user

@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(user_id: int, post: schemas.PostCreate, db = Depends(database.get_db)):
    post = crud.create_post(conn=db, post=post, user_id=user_id)

    if post is None:
        logger.error(f"Can not create post")
        raise HTTPException(status_code=404, detail="Can not create post")
    else:
        return post

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, db = Depends(database.get_db)):
    return crud.get_posts(conn=db, skip=skip, limit=limit)

@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db = Depends(database.get_db)):
    post = crud.get_post(conn=db, post_id=post_id)

    if post is None:
        logger.error(f"Post with ID {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db = Depends(database.get_db)):
    post = crud.update_post(conn=db, post_id=post_id, post=post)

    if post is None:
        logger.error(f"Post with ID {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db = Depends(database.get_db)):
    post = crud.delete_post(conn=db, post_id=post_id)

    if post is None:
        logger.error(f"Post with ID {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/users/{user_id}/posts/", response_model=list[schemas.Post])
def read_posts_by_user(user_id: int, db = Depends(database.get_db)):
    posts = crud.get_posts_by_user(conn=db, user_id=user_id)
    return posts

