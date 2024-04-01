from typing import Optional,Literal
from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from enum import Enum


class VoteEnum(Enum):
    DOWNVOTE = 'Down'
    UPVOTE = 'Up'

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at:datetime

    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResp(PostBase):

    id: int
    created_at: datetime
    owner: UserResp



    class Config:
        from_attributes = True

class AllPostResp(BaseModel):
    post: PostResp
    upvotes: int
    downvotes: int

    class Config:
        from_attributes = True
    
    


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)
    type: Literal["UPVOTE","DOWNVOTE"]