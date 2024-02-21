import os
import psycopg
from psycopg.rows import dict_row
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from dotenv import dotenv_values

config = dotenv_values()

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published: bool = True

# print(config.get("DATABASE_URL"))
conn = psycopg.connect(config.get("DATABASE_URL"),cursor_factory=psycopg.Cursor,row_factory=dict_row)

@app.get("/")
def root():
    return {
        "message" : "My API"
    }

@app.get("/posts")
def get_posts():

    rows = conn.execute(""" select * from posts """).fetchall()
    
    return {
        "data" : rows
    }

@app.post('/create_post', status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):

    cur = conn.execute(""" INSERT into posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                 (post.title,post.content,post.published))
    conn.commit()


    return {"data": cur.fetchone()}

@app.get("/posts/{id}")
def get_post(id:int):

    result = conn.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))   
    post = result.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return {"post details":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    
    result = conn.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = result.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):

    result = conn.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
                          (post.title,post.content,post.published,id))
    updated_post = result.fetchone()
    conn.commit()
    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} does nor exists")
    
    return {"data":updated_post}













