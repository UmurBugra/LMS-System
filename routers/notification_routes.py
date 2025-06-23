from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from schemas import LoginBase
from crud.notification import create_notification
from db.database import get_db
from db.models import NotificationData
from authentication.oauth2 import get_current_user_from_cookie

router = APIRouter(prefix="/notification", tags=["Notification"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_notifications(request: Request, db: Session = Depends(get_db), current_user: LoginBase = Depends(get_current_user_from_cookie)):
    notifications = db.query(NotificationData).filter(NotificationData.user_name == current_user.username).all()
    return templates.TemplateResponse("notifications.html", {"request": request, "notifications": notifications})