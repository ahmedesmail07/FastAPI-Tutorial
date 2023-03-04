from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..repo import blog


router = APIRouter(tags=["Blog"], prefix="/blog")
get_db = database.get_db


@router.get(
    "/", response_model=List[schemas.ShowBlog]
)  # Cause of u returns alist of blogs not only one
def GetBlogs(db: Session = Depends(database.get_db)):
    return blog.GetAllBlogs(db)


# Getting All Blogs FROM DB


@router.get(
    "/{id}", status_code=200, response_model=schemas.ShowBlog
)  # the default returned val== 200 (OK)
def GetParticularBlog(id, response: Response, db: Session = Depends(database.get_db)):
    return blog.ShowParticularBlog(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def DeleteParticularBlog(
    id, response: Response, db: Session = Depends(database.get_db)
):
    return blog.DeleteBlog(id, db)


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def UpdateParticularBlog(
    id, request: schemas.Blog, db: Session = Depends(database.get_db)
):
    return blog.UpdateBlog(id, request, db)


# Note that @app.patch is equal to app.put


@router.post("/", status_code=status.HTTP_201_CREATED)
def CreateBlog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.CreateBlog(request, db)
