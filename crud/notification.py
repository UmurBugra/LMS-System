from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db.models import NotificationData, LoginData, notification_receivers
from datetime import datetime, timedelta, timezone
from schemas import UserType

def create_notification(db: Session, content: str, receiver=None):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    notification_entry = NotificationData(
        content=content,
        created_time=turkey_time
    )

    if receiver:
        notification_entry.receiver = receiver

    db.add(notification_entry)
    db.commit()
    db.refresh(notification_entry)
    return notification_entry

def create_notification_for_all_students(db: Session, content: str, sender_username: str):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    students = db.query(LoginData).filter(LoginData.type == UserType.student).all()

    notification = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_username=sender_username
    )
    notification.receiver = students

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification 

def create_notification_for_all_teachers(db: Session, content: str, sender_id: int):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    sender = db.query(LoginData).filter(LoginData.id == sender_id).first()
    if not sender:
        raise ValueError("Geçersiz kullanıcı ID'si")

    teachers = db.query(LoginData).filter(LoginData.type == UserType.teacher,
                                          LoginData.id != sender_id).all()

    notification = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_username=sender.username
    )
    notification.receiver = teachers

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notifications(db: Session, username: str):
    user = db.query(LoginData).filter(LoginData.username == username).first()
    if user:
        return user.notifications
    return []

def clear_notifications(db: Session, current_user: LoginData):
    try:
        user = db.query(LoginData).filter(
            LoginData.username == current_user.username,
            LoginData.id == current_user.id
        ).first()

        if not user:
            raise ValueError("Kullanıcı bulunamadı.")

        else:
            db.execute(
                notification_receivers.update().where(
                    notification_receivers.c.user_id == user.id
                ).values(is_removed=True)
            )
            db.commit()
            return JSONResponse({"message": "Tüm bildirimler başarıyla silindi."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







