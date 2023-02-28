from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "Welcome To Fast Api"}


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
