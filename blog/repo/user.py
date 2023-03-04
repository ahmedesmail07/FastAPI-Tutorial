from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..hashing import Hash


def CreateNewUser(request: schemas.UserCreate, db: Session):
    new_user = models.UserCreate(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def ShowUser(id: int, db: Session):
    user = db.query(models.UserCreate).filter(models.UserCreate.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no blog with this id num",
        )
    return user
