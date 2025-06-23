from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.templating import Jinja2Templates
from authentication.oauth2 import get_current_user_from_cookie
from schemas import UserType
from db.models import NotificationData

router = APIRouter(prefix="/nav", tags=["navigation"])
templates = Jinja2Templates(directory="templates")

# Çıkış yapma işlemi
@router.get("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    response = RedirectResponse(url="/", status_code=302) # oturum sonlandırma # HTTP 302 (Found/Redirect)
    response.delete_cookie("access_token")                # çerez silme
    return response

@router.get("/home")
def go_to_home(request: Request, db: Session = Depends(get_db), current_user = Depends(get_current_user_from_cookie)):

    if current_user.type == UserType.student:
        display_user_type = "Öğrenci"
    elif current_user.type == UserType.teacher:
        display_user_type = "Öğretmen"
    else:
        display_user_type = "Bilinmiyor"

    notifications = db.query(NotificationData).filter(NotificationData.user_name == current_user.username).all()

    return templates.TemplateResponse( "home.html",
                                       {"request": request,
                                        "username": current_user.username,
                                        "user_type": display_user_type,
                                        "notifications": notifications
                                        })
