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
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    login_request = LoginEmailPassword(email=email, password=password)
    result = auth.user_login(db, login_request)

    if isinstance(result, str):
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": result}
        )
    else:
        # Token oluşturma ve cookie ayarlama
        access_token = oauth2.create_access_token(data={"sub": result["email"]})
        response = RedirectResponse(url="/nav/home", status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response