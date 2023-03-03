from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
