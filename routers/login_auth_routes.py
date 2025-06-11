from fastapi import APIRouter, Depends, Form, Request
from schemas import LoginBase, AuthUserType, UserType, LoginEmailPassword
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates
from db.models import LoginData
from fastapi.responses import RedirectResponse

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
def user_login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(LoginData).filter(
        LoginData.email == email,
        LoginData.password == password
    ).first()

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "E-posta veya şifre yanlış"}
        )
    else:
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "email": user.email}
        )