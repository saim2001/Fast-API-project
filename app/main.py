from fastapi import FastAPI,Depends
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session
from .routers import post,user


models.Base.metadata.create_all(bind=engine)



app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)

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
















