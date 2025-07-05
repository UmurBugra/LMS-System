from fastapi import APIRouter, Depends, Form, Request, Response
from schemas import LoginEmailPassword
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from authentication import oauth2

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

# Form verilerini işlemek için yeni endpoint
@router.post("/login/form")
def user_login_form(
        request: Request,
        login_form: LoginEmailPassword = Depends(LoginEmailPassword.form),
        db: Session = Depends(get_db)
):
    result = auth.user_login(db, login_form)

    if isinstance(result, str):                 # eğer result bir hata mesajıysa(str) isinstance --> True
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": result}
        )
    else:
        access_token = oauth2.create_access_token(      # access_token bu şekilde döner.
            data={
                "sub": result["email"],         # benzersiz tanımlayıcı olarak email seçtim fakat ID de kullanılabilir.
                "user_id": result["id"],
                "user_type": result["user_type"],
                "email": result["email"],
                "username": result["username"]  # Eğer varsa
            }
        )
        print("TOKEN:", access_token)          # Token'ı konsola yazdırdım, bazen gerek oluyor.
        if result["user_type"] == "admin":     # Eğer kullanıcı admin ise admin sayfasına yönlendir.
            redirect_url = "/nav/admin-home"
        else:
            redirect_url = "/nav/home"         # Eğer kullanıcı normal bir kullanıcı ise home sayfasına yönlendir.
        response = RedirectResponse(url=redirect_url, status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True) # Token'ı cookie olarak ayarladım.
        return response