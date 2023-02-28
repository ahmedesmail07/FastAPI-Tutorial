from fastapi import FastAPI
from . import schemas, models  # dot is meaning import from the current dir
from .database import engine

models.Base.metadata.create_all(engine)

# when u use schemas then when u extends a class from it
# u should first type schemas.className then it will be working


app = FastAPI()
# u can use this inner app using uvicon after installation of req.txt by using commang:
# uvicorn blog.main:app --reload


@app.post("/blog")
def CreatePost(request: schemas.Blog):
    return request
