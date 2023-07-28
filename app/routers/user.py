from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import session, engine, Base, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    """hashing the password"""
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    """user = db.query(models.User).filter(models.User.email == user.email)
    if user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Email already taken")
                            """
    newUser = models.User(**user.model_dump())

    """checking if email is unique"""
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    user_found = user.first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found")
    return user_found

