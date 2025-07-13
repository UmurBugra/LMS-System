from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import LoginBase
from crud.notification import create_notification, get_notifications,create_notification_for_all_students, \
create_notification_for_all_teachers, soft_delete_notifications, notification_detail
from db.database import get_db
from authentication.oauth2 import get_current_user_from_cookie
from db.models import NotificationData

router = APIRouter(prefix="/notification", tags=["Notification"])
templates = Jinja2Templates(directory="templates")

# Bildirimleri listeleme
@router.get("/")
def get_notifications_route(request: Request, db: Session = Depends(get_db), current_user: LoginBase = Depends(get_current_user_from_cookie)):
    notifications = get_notifications(db, current_user.username, current_user.id)

    # Kullanıcı tipini belirle
    if current_user.type.name == "student":
        display_user_type = "Öğrenci"
    elif current_user.type.name == "teacher":
        display_user_type = "Öğretmen"
    elif current_user.type.name == "admin":
        display_user_type = "Admin"
    else:
        display_user_type = "Bilinmiyor"

    return templates.TemplateResponse("notifications.html", {
        "request": request,
        "notifications": notifications,
        "username": current_user.username,
        "user_type": display_user_type
    })

# Bildirim oluşturma
@router.post("/create")
def create_notification_route(
    content: str = Form(...),
    receiver: str = Form(None),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(get_current_user_from_cookie)
):
    if not content:
        raise HTTPException(status_code=400, detail="boş duyuru içeriği")

    try:
        if receiver == "all_students":
            create_notification_for_all_students(db, content, sender_id=current_user.id)
        elif receiver == "all_teachers":
            create_notification_for_all_teachers(db, content, sender_id=current_user.id)
        else:
            create_notification(db, content, sender_id=current_user.id, receiver=None)
        return JSONResponse({"message": "Duyuru başarıyla gönderildi."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tek bildirimi görüntüleme
@router.get("/{notification_id}")
def get_notification_detail(
    notification_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(get_current_user_from_cookie)
):

    notification = notification_detail(db, notification_id, current_user)

    all_notifications = get_notifications(db, current_user.username, current_user.id)

    if not notification:
        raise HTTPException(status_code=404, detail="Bildirimi bulunamadı.")

    if current_user.type.name == "student":
        display_user_type = "Öğrenci"
    elif current_user.type.name == "teacher":
        display_user_type = "Öğretmen"
    elif current_user.type.name == "admin":
        display_user_type = "Admin"
    else:
        display_user_type = "Bilinmiyor"

    notification_entry = db.query(NotificationData).filter(NotificationData.id == notification_id).first()

    # Eğer redirect_url varsa ve "/calendar/" içeriyorsa takvim detay sayfasına yönlendir
    if notification_entry and notification_entry.redirect_url and "/calendar/" in notification_entry.redirect_url:
        calendar_id = notification_entry.redirect_url.split("/")[-1]
        return RedirectResponse(url=f"/calendar/{calendar_id}")

    return templates.TemplateResponse("notification_detail.html", {
        "request": request,
        "notification": notification,
        "username": current_user.username,
        "user_type": display_user_type,
        "notifications": all_notifications
    })

# Tüm bildirimleri silme (soft delete)
@router.put("/clear-all")
def soft_delete_all_notifications(
        db: Session = Depends(get_db),
        current_user: LoginBase = Depends(get_current_user_from_cookie)
):
    soft_delete_notifications(db, current_user)