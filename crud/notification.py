from sqlalchemy.orm import Session
from db.models import NotificationData, LoginData


def create_notification(db: Session, content: str, username: str):
    notification_entry = NotificationData(
        content=content,
        user_name=username
    )
    db.add(notification_entry)
    db.commit()
    db.refresh(notification_entry)
    return notification_entry

def create_notification_for_all_students(db: Session, content: str):
    students = db.query(LoginData).filter(LoginData.type == "Öğrenci").all()
    for student in students:
        create_notification(db, content, student.username)