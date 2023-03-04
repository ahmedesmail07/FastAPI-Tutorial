from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List


def GetAllBlogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def CreateBlog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def DeleteBlog(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no blog with this id num",
        )
    blog.delete(synchronize_session=False)

    db.commit()  # Don't forget it to save the changes of the DELETION
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="This Blog Has Been Deleted Succesfully"
    )


def UpdateBlog(id: int, request: schemas, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no blog with this id num",
        )
    blog.update(request.dict())
    # Update Fields REQUIRED // when u put request parameter it will update all parts
    db.commit()
    return "UPDATED SUCCESFULLY"


def ShowParticularBlog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog with the id of {id} in not created yet"}
    return blog
