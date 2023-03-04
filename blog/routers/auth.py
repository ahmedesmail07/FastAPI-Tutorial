from fastapi import APIRouter
from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
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
    return user
