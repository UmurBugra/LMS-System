from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import LoginBase
from crud.notification import create_notification, get_notifications, create_notification_for_all_students
from db.database import get_db
from authentication.oauth2 import get_current_user_from_cookie

router = APIRouter(prefix="/notification", tags=["Notification"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_notifications_route(request: Request, db: Session = Depends(get_db), current_user: LoginBase = Depends(get_current_user_from_cookie)):
    notifications = get_notifications(db, current_user.username)
    return templates.TemplateResponse("notifications.html", {"request": request, "notifications": notifications})

@router.post("/create")
def create_notification_route(
    content: str = Form(...),
    recipients: str = Form(None),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(get_current_user_from_cookie)
):
    if not content:
        raise HTTPException(status_code=400, detail="boş duyuru içeriği")

    try:
        if recipients == "all":
            create_notification_for_all_students(db, content, sender_username=current_user.username)
            response = RedirectResponse(url="/nav/home", status_code=303) # 303 sonucu başka url üzerine yönlendirir
            return response
        else:
            create_notification(db, content, current_user.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))