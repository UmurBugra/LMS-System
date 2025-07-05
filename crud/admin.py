from sqlalchemy import or_, cast, String
from sqlalchemy.orm import Session
from schemas import UserType, LoginBase
from db.models import LoginData, NotificationData
from datetime import datetime, timezone, timedelta

#CRUD operations for admin
# Create user
def create_user_by_admin(db: Session, request, user_type: UserType):
    new_user = LoginData(
        username=request.username,
        password=request.password,
        email=request.email,
        type=user_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Read all users
def get_read_users_by_admin(db: Session):
    return db.query(LoginData).all()

# Update user
def update_user_by_admin(db: Session, id: int, request: LoginBase, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.id == id)
    user.update({
        "username": request.username,
        "password": request.password,
        "email": request.email,
        "type": user_type
    })
    db.commit()
    return user.first()

# Delete user
def delete_user_by_admin(db: Session, id: int):
    user = db.query(LoginData).filter(LoginData.id == id).first()
    if user:
        db.delete(user)
        db.commit()
    return "Kullanıcı silindi"

# Create notification for everyone
def create_notification_for_everyone(db: Session, content: str, sender_id: int):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    admin = db.query(LoginData).filter(LoginData.id == sender_id).first()
    if not admin:
        raise ValueError("Geçersiz kullanıcı ID'si")

    ignore_admin = db.query(LoginData).filter(LoginData.id != sender_id).all()

    notification = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_username=admin.username
    )
    notification.receiver = ignore_admin
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

# Search users
def search_users(db: Session, query: str):

    if not query:
        return []

    users = db.query(LoginData).filter(
        or_(                                                # --> 3 alan üzerinden arama yapılıyor.
            LoginData.username.like(f"%{query}%"),
            LoginData.email.like(f"%{query}%"),
            cast(LoginData.id, String).like(f"%{query}%")   # --> ID str olarak çevirilip aranıyor.
        )).limit(10).all()

    return {"users": users}