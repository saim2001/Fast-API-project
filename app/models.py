from .database import Base
from sqlalchemy.orm import Relationship
from sqlalchemy import TIMESTAMP, Column,Integer,VARCHAR,Boolean,String,ForeignKey
from sqlalchemy.sql.expression import text


class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(VARCHAR,nullable=False)
    content = Column(VARCHAR,nullable=False)
    published = Column(Boolean,server_default="True",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner = Relationship("User") 


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(VARCHAR,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(VARCHAR,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


