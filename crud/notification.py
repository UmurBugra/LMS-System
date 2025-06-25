from sqlalchemy.orm import Session
from db.models import NotificationData, LoginData
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

def get_notifications(db: Session, username: str):
    user = db.query(LoginData).filter(LoginData.username == username).first()
    if user:
        return user.notifications
    return []