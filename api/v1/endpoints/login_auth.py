from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from schemas import LoginEmailPassword
from crud import auth
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from authentication import oauth2

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

# API için JSON login endpoint (Swagger UI için)
@router.post("/login/api")
def user_login_api(
    login_form: LoginEmailPassword,
    db: Session = Depends(get_db)
):
    """
    API Login endpoint for Swagger UI
    Returns JWT token for authentication
    """
    result = auth.user_login(db, login_form)

    if isinstance(result, str):
        raise HTTPException(status_code=401, detail=result)

    access_token = oauth2.create_access_token(
        data={
            "sub": result["email"],
            "user_id": result["id"],
            "user_type": result["user_type"],
            "email": result["email"],
            "username": result["username"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": result["user_type"],
        "user_id": result["id"]
    }

# Form verilerini işlemek için yeni endpoint
@router.post("/login/form")
def user_login_form(
        request: Request,
        login_form: LoginEmailPassword = Depends(LoginEmailPassword.form),
        db: Session = Depends(get_db)
):
    result = auth.user_login(db, login_form)

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
                "username": result["username"]
            }
        )
        print(access_token)
        if result["user_type"] == "admin":
            redirect_url = "/api/v1/nav/admin-home"
        else:
            redirect_url = "/api/v1/nav/home"
        response = RedirectResponse(url=redirect_url, status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response

# OAuth2 standart token endpoint (Swagger UI için)
@router.post("/token")
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token endpoint
    Use username as email field
    """
    # OAuth2PasswordRequestForm'da username field'ı var, biz bunu email olarak kullanacağız
    login_form = LoginEmailPassword(email=form_data.username, password=form_data.password)

    result = auth.user_login(db, login_form)

    if isinstance(result, str):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = oauth2.create_access_token(
        data={
            "sub": result["email"],
            "user_id": result["id"],
            "user_type": result["user_type"],
            "email": result["email"],
            "username": result["username"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
