from fastapi import APIRouter
from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..hashing import Hash
from .. import token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.UserCreate)
        .filter(models.UserCreate.email == request.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password"
        )
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
