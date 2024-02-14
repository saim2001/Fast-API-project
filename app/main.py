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
    pulished: bool = True

print(config.get("DATABASE_URL"))
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










