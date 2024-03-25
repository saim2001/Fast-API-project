from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime


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
    


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None