from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models  # dot is meaning import from the current dir
from .database import engine, SessionLocal


models.Base.metadata.create_all(
    bind=engine
)  # if u find any model let us create it into db

# when u use schemas then when u extends a class from it
# u should first type schemas.className then it will be working


app = FastAPI()


# u can use this inner app using uvicon after installation of req.txt by using commang:
# uvicorn blog.main:app --reload
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def CreatePost(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get(
    "/blog", response_model=List[schemas.ShowBlog]
)  # Cause of u returns alist of blogs not only one
def GetBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Getting All Blogs FROM DB


@app.get(
    "/blog/{id}", status_code=200, response_model=schemas.ShowBlog
)  # the default returned val== 200 (OK)
def GetParticularBlog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog with the id of {id} in not created yet"}
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def DeleteParticularBlog(id, response: Response, db: Session = Depends(get_db)):
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


@app.patch("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def UpdateParticularBlog(id, request: schemas.Blog, db: Session = Depends(get_db)):
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


@app.post("/user")
def CreateUser(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.UserCreate(
        name=request.name, email=request.email, password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
