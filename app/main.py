import os
import psycopg
from psycopg.rows import dict_row
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app = FastAPI()



class Post(BaseModel):
    title : str
    content : str
    published: bool = True

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

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    
    return {
        "data" : posts
    }

@app.post('/create_post', status_code= status.HTTP_201_CREATED)
def create_posts(post: Post,db: Session = Depends(get_db)):

    # cur = conn.execute(""" INSERT into posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #              (post.title,post.content,post.published))
    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return {"post details":post}

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


@app.put("/posts/{id}")
def update_post(id:int,post:Post,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()


    if post_data ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} does nor exists")
    
    print(post.model_dump_json())
    post_query.update({
        "title" : post.title,
        "content" : post.content,
        "published" : post.published
    },synchronize_session=False)
    db.commit()
    
    return {"data":post_query.first()}













