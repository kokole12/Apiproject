from fastapi import APIRouter, HTTPException, Depends, Response, status
from ..database import get_db, engine
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.AccessToken)
def login(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    """verifying the passwords"""
    if not utils.verifyPassword(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND,
                            detail=f"Invalid Credentials")

    """create token"""
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    """return the token"""
    return {"access_token": access_token, "token_type": "Bearer"}
