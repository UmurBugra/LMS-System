from sqlalchemy.orm import Session
from db.models import NotificationData, LoginData
from datetime import datetime, timedelta, timezone
from schemas import UserType

def create_notification(db: Session, content: str, receiver=None):
    turkey_tz = timezone(timedelta(hours=3))
    current_time = datetime.now(turkey_tz)

    notification_entry = NotificationData(
        content=content,
        created_time=current_time
    )

    if receiver:
        notification_entry.receiver = receiver

    db.add(notification_entry)
    db.commit()
    db.refresh(notification_entry)
    return notification_entry

def create_notification_for_all_students(db: Session, content: str, sender_username: str):
    students = db.query(LoginData).filter(LoginData.type == UserType.student).all()

    notification = NotificationData(
        content=content,
        sender_username=sender_username
    )
    db.add(notification)

    notification.receiver = students

    db.commit()
    db.refresh(notification)
    return notification

def get_notifications(db: Session, username: str):
    user = db.query(LoginData).filter(LoginData.username == username).first()
    if user:
        return user.notifications
    return []