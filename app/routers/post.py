from .. import models,schema
from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("",response_model=List[schema.PostResp])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user),
              limit: int = 10,search: Optional[str] = ""):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    return posts

@router.post('', status_code= status.HTTP_201_CREATED,response_model=schema.PostResp)
def create_posts(post: schema.PostCreate,db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # cur = conn.execute(""" INSERT into posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #              (post.title,post.content,post.published))
    # conn.commit()
    # print(user_id)
    new_post = models.Post(owner_id=user_id.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post

@router.get("/{id}",response_model=schema.PostResp)
def get_post(id:int,db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    
    if post.first().owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.PostResp)
def update_post(id:int,post:schema.PostCreate,db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)    ):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()


    if post_data ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} not found")
    
    if post_data.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    
    post_query.update({
        "title" : post.title,
        "content" : post.content,
        "published" : post.published
    },synchronize_session=False)
    db.commit()
    
    return post_query.first()