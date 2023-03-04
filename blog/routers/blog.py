from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Blog"], prefix="/blog")


@router.get(
    "/", response_model=List[schemas.ShowBlog]
)  # Cause of u returns alist of blogs not only one
def GetBlogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Getting All Blogs FROM DB


@router.get(
    "/{id}", status_code=200, response_model=schemas.ShowBlog
)  # the default returned val== 200 (OK)
def GetParticularBlog(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog with the id of {id} in not created yet"}
    return blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def DeleteParticularBlog(
    id, response: Response, db: Session = Depends(database.get_db)
):
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


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def UpdateParticularBlog(
    id, request: schemas.Blog, db: Session = Depends(database.get_db)
):
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


# Note that @app.patch is equal to app.put


@router.post("/", status_code=status.HTTP_201_CREATED)
def CreateBlog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
