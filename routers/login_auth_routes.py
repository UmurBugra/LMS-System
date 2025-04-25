from fastapi import APIRouter, Depends
from schemas import LoginDisplay, LoginBase, AuthUserType, UserType
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# User student or teacher
@router.post("/")
def user_type_request(request: AuthUserType, db: Session = Depends(get_db)):
    return auth.user_type_request(db, request)

# User Login Control
@router.post("/login")
def user_login(request: LoginBase, user_type: UserType ,db: Session = Depends(get_db)):
    return auth.user_login(db, request, user_type)

