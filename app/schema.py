from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResp(PostBase):

    
    created_at: datetime

    class Config:
        from_attributes = True
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
    
    