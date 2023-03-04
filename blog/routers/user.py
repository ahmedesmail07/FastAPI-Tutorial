from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..hashing import Hash

router = APIRouter(prefix="/user",tags=["User"])


@router.post("/", response_model=schemas.ShowUser )
def CreateUser(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = models.UserCreate(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.ShowUser)
def GetUser(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.UserCreate).filter(models.UserCreate.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no blog with this id num",
        )
    return user
