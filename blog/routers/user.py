from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..hashing import Hash
from ..repo import blog, user

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=schemas.ShowUser)
def CreateUser(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return user.CreateNewUser(request, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def GetUser(id: int, db: Session = Depends(database.get_db)):
    return user.ShowUser(id, db)
