from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models  # dot is meaning import from the current dir
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

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


@app.get("/blog")
def GetBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Getting All Blogs FROM DB


@app.get("/blog/{id}", status_code=200)  # the default returned val== 200 (OK)
def GetParticularBlog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog with the id of {id} in not created yet"}
    return blog