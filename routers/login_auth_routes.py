from fastapi import APIRouter, Depends, Form, Request
from schemas import LoginBase, AuthUserType, UserType
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

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
def process_login(request: Request,
                username: str = Form(...),
                password: str = Form(...),
                email: str = Form(...),
                user_type: UserType = Form(...),
                db: Session = Depends(get_db)):

    login_data = LoginBase(username=username, password=password, email=email)
    result = auth.user_login(db, login_data, user_type) # Kullanıcının bilgileri doğru girip girmediğini kontrol et
    if result == "Giriş yapıldı":   # Fonksiyonun döndürdüğü değer "Giriş yapıldı" ise
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "username": username, "email": email, "user_type": user_type}
        )
    else:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": result}
        )