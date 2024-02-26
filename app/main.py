import os
import psycopg
from psycopg.rows import dict_row
from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session
from .schema import PostBase,PostCreate,PostResp,UserCreate

models.Base.metadata.create_all(bind=engine)



app = FastAPI()





# # print(config.get("DATABASE_URL"))
# conn = psycopg.connect(config.get("DATABASE_URL"),cursor_factory=psycopg.Cursor,row_factory=dict_row)

@app.get("/")
def root():
    return {
        "message" : "My API"
    }

@app.get("/test")
def test(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {
        "message" : posts
    }

@app.get("/posts",response_model=List[PostResp])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    
    return posts

@app.post('/create_post', status_code= status.HTTP_201_CREATED,response_model=PostResp)
def create_posts(post: PostCreate,db: Session = Depends(get_db)):

    # cur = conn.execute(""" INSERT into posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #              (post.title,post.content,post.published))
    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post

@app.get("/posts/{id}",response_model=PostResp)
def get_post(id:int,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=PostResp)
def update_post(id:int,post:PostCreate,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()


    if post_data ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} not found")
    
    post_query.update({
        "title" : post.title,
        "content" : post.content,
        "published" : post.published
    },synchronize_session=False)
    db.commit()
    
    return post_query.first()

@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user












