from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import LoginData
from schemas import UserType
from authentication import oauth2

router = APIRouter(
    tags=["authentication"]
)
@router.post("/token") # tokenUrl ile aynı olmalı.
def get_token(request: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(LoginData).filter(LoginData.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hatalı giriş bilgileri. Lütfen tekrar deneyin.",
        )
    if user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hatalı giriş bilgileri. Lütfen tekrar deneyin.",
        )

    access_token = oauth2.create_access_token(data={"sub": user.email, "user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }