from fastapi import APIRouter, Depends, Form
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

# Form verilerini işlemek için yeni endpoint
# Arayüz giriş kısmında form verisi gönderiyordum fakat benden query bekliyordu bu şekilde form body den veriyi alıyor.
@router.post("/login/form")
def process_login(username: str = Form(...),
                  password: str = Form(...),
                  email: str = Form(...),
                  user_type: UserType = Form(...),
                  db: Session = Depends(get_db)):

    login_data = LoginBase(username=username, password=password, email=email)
    result = auth.user_login(db, login_data, user_type)
    if result == "Giriş yapıldı":
        return {"message": "Giriş başarılı"}
    else:
        return {"message": "Giriş başarısız. Hatalı bilgiler."}