from fastapi import FastAPI
from . import models  # dot is meaning import from the current dir
from .database import engine
from .routers import blog, user, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

models.Base.metadata.create_all(
    bind=engine
)  # if u find any model let us create it into db

# when u use schemas then when u extends a class from it
# u should first type schemas.className then it will be working


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)


app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)

# u can use this inner app using uvicon after installation of req.txt by using commang:
# uvicorn blog.main:app --reload
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blog"])
# def CreateBlog(request: schemas.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog


# @app.get(
#     "/blog", response_model=List[schemas.ShowBlog], tags=["Blog"]
# )  # Cause of u returns alist of blogs not only one
# def GetBlogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


# # Getting All Blogs FROM DB


# @app.get(
#     "/blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=["Blog"]
# )  # the default returned val== 200 (OK)
# def GetParticularBlog(id, response: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {f"Blog with the id of {id} in not created yet"}
#     return blog


# @app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
# def DeleteParticularBlog(id, response: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="There is no blog with this id num",
#         )
#     blog.delete(synchronize_session=False)

#     db.commit()  # Don't forget it to save the changes of the DELETION
#     raise HTTPException(
#         status_code=status.HTTP_200_OK, detail="This Blog Has Been Deleted Succesfully"
#     )


# @app.patch("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blog"])
# def UpdateParticularBlog(id, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="There is no blog with this id num",
#         )
#     blog.update(request.dict())
#     # Update Fields REQUIRED // when u put request parameter it will update all parts
#     db.commit()
#     return "UPDATED SUCCESFULLY"


# # Note that @app.patch is equal to app.put


# @app.post("/user", response_model=schemas.ShowUser, tags=["User"])
# def CreateUser(request: schemas.UserCreate, db: Session = Depends(get_db)):
#     new_user = models.UserCreate(
#         name=request.name,
#         email=request.email,
#         password=Hash.bcrypt(request.password),
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get("/user/{id}", response_model=schemas.ShowUser, tags=["User"])
# def GetUser(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.UserCreate).filter(models.UserCreate.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="There is no blog with this id num",
#         )
#     return user
