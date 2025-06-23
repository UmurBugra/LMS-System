from sqlalchemy.orm import Session
from db.models import NotificationData, LoginData
from datetime import datetime, timedelta, timezone
from schemas import UserType

def create_notification(db: Session, content: str, username: str):
    turkey_tz = timezone(timedelta(hours=3))
    current_time = datetime.now(turkey_tz)

    notification_entry = NotificationData(
        content=content,
        user_name=username,
        created_time=current_time
    )
    db.add(notification_entry)
    db.commit()
    db.refresh(notification_entry)
    return notification_entry

def create_notification_for_all_students(db: Session, content: str):
    students = db.query(LoginData).filter(LoginData.type == UserType.student).all()
    for student in students:
        create_notification(db, content, student.username)

def get_notifications(db: Session, username: str):
    notifications = db.query(NotificationData).filter(NotificationData.user_name == username).all()
    return notifications