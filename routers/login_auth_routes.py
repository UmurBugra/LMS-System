from fastapi import APIRouter, Depends, Form, Request, Response
from schemas import LoginBase, AuthUserType, UserType, LoginEmailPassword
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates
from db.models import LoginData
from fastapi.responses import RedirectResponse
from authentication import oauth2
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
        response: Response,  # Response parametresini ekleyin
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
            "index.html",
            {"request": request, "error": "E-posta veya şifre yanlış"}
        )
    else:
        display_user_type = ""
        if user.type == UserType.student:
            display_user_type = "Öğrenci"
        elif user.type == UserType.teacher:
            display_user_type = "Öğretmen"

        # Token oluştur ve cookie'ye ekle
        access_token = oauth2.create_access_token(data={"sub": user.username})
        response = templates.TemplateResponse(
            "home.html",
            {"request": request, "username": user.username, "user_type": display_user_type}
        )
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
# Çıkış yapma işlemi
@router.get("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    response = RedirectResponse(url="/", status_code=302) # oturum sonlandırma # HTTP 302 (Found/Redirect)
    response.delete_cookie("access_token")                  # çerez silme
    return response