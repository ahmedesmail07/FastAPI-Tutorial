from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(
        String,
    )
    body = Column(String)
    user_id = Column(Integer, ForeignKey("UserCreate.id"))
    creator = relationship("UserCreate", back_populates="blogs")


class UserCreate(Base):
    __tablename__ = "UserCreate"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="creator")


# when you create a blog or when you get the users it is known that the creator of
# the blog must be a user and also if u need to get the user u should be able to
# see the blogs which is created by himself so it is clearly that we need to use
# relation ship between the blog & the user so how to do this ? let's go
