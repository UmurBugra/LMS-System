from fastapi import APIRouter, Depends, Form, Request, Response
from schemas import LoginBase, AuthUserType, UserType, LoginEmailPassword
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from authentication import oauth2

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

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
        access_token = oauth2.create_access_token(
            data={
                "sub": result["email"],
                "user_id": result["id"],
                "user_type": result["user_type"],
                "email": result["email"],
                "username": result["username"]  # Eğer varsa
            }
        )
        print("TOKEN:", access_token)
        if result["user_type"] == "admin":
            redirect_url = "/nav/admin-home"
        else:
            redirect_url = "/nav/home"
        response = RedirectResponse(url=redirect_url, status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response