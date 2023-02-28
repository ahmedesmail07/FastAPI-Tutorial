from fastapi import FastAPI, Depends
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


@app.post("/blog")
def CreatePost(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
