from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from db.models import NotificationData, LoginData, notification_receivers
from datetime import datetime, timedelta, timezone
from schemas import UserType

def create_notification(db: Session, content: str, sender_username=None, receiver=None):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    notification_entry = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_username=sender_username
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


# Kullanıcıya ait bildirimleri getir
def get_notifications(db: Session, username: str):
    user = db.query(LoginData).filter(LoginData.username == username).first()
    if user:
        notifications = db.query(NotificationData).join(
            notification_receivers,
            (NotificationData.id == notification_receivers.c.notification_id)
        ).filter(
            notification_receivers.c.user_id == (user.id),
            notification_receivers.c.is_removed == False
        ).all()
        return notifications
    return []

def soft_delete_notifications(db: Session, current_user: LoginData):
    try:
        user = db.query(LoginData).filter(
            LoginData.username == current_user.username,
            LoginData.id == current_user.id
        ).first()

        if not user:
                raise ValueError("Kullanıcı bulunamadı.")

        utc_now = datetime.now(timezone.utc)
        turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))


        db.execute(
            notification_receivers.update().where(
                notification_receivers.c.user_id == user.id
            ).values(is_removed=True, is_removed_time=turkey_time)
        )
        db.commit()

        return JSONResponse(status_code=200, content={"message": "Bildirimler silindi."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))