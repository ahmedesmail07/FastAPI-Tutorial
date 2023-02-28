from fastapi import FastAPI
from typing import (
    Optional,
)  # Don't forget to import it for making sure optional works at sort parameter

app = FastAPI()


@app.get("/blog")
def index(  # in this case it is REQUIRED VALUES note that okay ?
    limit, published, sort: Optional[str] = None
):  # if u set published = bool in the query it will be returned as a boolean value not string
    if published:
        return {"data": f"{limit} from blog DB"}
    else:
        return {"data": f"{limit} from blog DB if unpublished "}


# this published value will be return this values if we set the published parameter== true
# in the route(PATH) of the url >> localhost:8000/blogs/published=true


@app.get("/blog/{id}")
def show(id: int):  # returns only integer value in the url path
    return {"DATA": id}


# ALWAYS set the dynamic function in the bottom of

# this function unpublished()will return an error because of fast is reading the app line by line
# so if u tried to do this it will be string value but in the above function
# i set it as an integer value so unpublished is a string value so it will not working
# if u set as above the show function it will be working due to it is a DYNAIMC ROUTE

# @app.get("blog/unpublished")
# def unpublished():
#     return {"This is all unpublished blogs "}


@app.get("/blog/{id}/comments")
def comments(id: int):
    return {"Data": {"Comments Is Here For ID ": id}}
