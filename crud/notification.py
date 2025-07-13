from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.responses import JSONResponse
from db.models import NotificationData, LoginData, notification_receivers
from datetime import datetime, timedelta, timezone
from schemas import UserType

# Bildirim oluşturma işlemleri
# Bu fonksiyon, belirtilen içeriğe sahip bir bildirim oluşturur.
def create_notification(db: Session, content: str, sender_id: int, receiver=None):
    utc_now = datetime.now(timezone.utc)                                # --> UTC zamanını al
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))     # --> Türkiye saat dilimine dönüştür

    notification_entry = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_id=sender_id
    )

    db.add(notification_entry)
    db.commit()
    db.refresh(notification_entry)

    if receiver:
        if isinstance(receiver, list):
            for user in receiver:
                db.execute(
                    notification_receivers.insert().values(
                        user_id=user.id,
                        notification_id=notification_entry.id,
                        is_read=False,
                        is_removed=False
                    )
                )
        else:
            db.execute(
                notification_receivers.insert().values(
                    user_id=receiver.id,
                    notification_id=notification_entry.id,
                    is_read=False,
                    is_removed=False
                )
            )
        db.commit()

    return notification_entry

# Bu fonksiyon, tüm öğrencilere bir bildirim gönderir.
def create_notification_for_all_students(db: Session, content: str, sender_id: int):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    students = db.query(LoginData).filter(LoginData.type == UserType.student).all()

    notification = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_id=sender_id,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    notification.redirect_url = f"/notification/{notification.id}"
    db.commit()

    # Her öğrenci için notification_receivers tablosuna kayıt ekle
    for student in students:
        db.execute(
            notification_receivers.insert().values(
                user_id=student.id,
                notification_id=notification.id,
                is_read=False,
                is_removed=False
            )
        )

    db.commit()
    return notification

# Bu fonksiyon, tüm öğretmenlere bir bildirim gönderir.
def create_notification_for_all_teachers(db: Session, content: str, sender_id: int):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=+3)))

    sender = db.query(LoginData).filter(LoginData.id == sender_id).first()
    if not sender:
        raise ValueError("Geçersiz kullanıcı ID'si")

    teachers = db.query(LoginData).filter(
        LoginData.type == UserType.teacher,
        LoginData.id != sender_id
    ).all()

    notification = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_id=sender_id
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    notification.redirect_url = f"/notification/{notification.id}"

    # Her öğretmen için notification_receivers tablosuna kayıt ekle
    for teacher in teachers:
        db.execute(
            notification_receivers.insert().values(
                user_id=teacher.id,
                notification_id=notification.id,
                is_read=False,
                is_removed=False
            )
        )

    db.commit()
    return notification

def calendar_notification_for_student(db: Session, calendar_entry, content: str ,sender_id: int):
    utc_now = datetime.now(timezone.utc)
    turkey_time = utc_now.astimezone(timezone(timedelta(hours=3)))

    students = db.query(LoginData).filter(LoginData.type == UserType.student).all()

    notification = NotificationData(
        content=content,
        created_time=turkey_time,
        sender_id=sender_id,
        redirect_url=f"/calendar/{calendar_entry.id}"
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Her öğrenci için notification_receivers tablosuna kayıt ekle
    for student in students:
        db.execute(
            notification_receivers.insert().values(
                user_id=student.id,
                notification_id=notification.id,
                is_read=False,
                is_removed=False
            )
        )

    db.commit()
    return notification

# Kullanıcıya ait bildirimleri getir
# Bu fonksiyon, belirtilen kullanıcı adı ve kullanıcı ID'sine sahip kullanıcının bildirimlerini getirir.
def get_notifications(db: Session, username: str, user_id: int):
    user = db.query(LoginData).filter(
        LoginData.username == username,
    LoginData.id == user_id).first()

    if user:

        notifications = db.query(NotificationData, notification_receivers.c.is_read).join(
            notification_receivers,
            NotificationData.id == notification_receivers.c.notification_id
        ).filter(
            notification_receivers.c.user_id == user.id,
            notification_receivers.c.is_removed == False
        )

        bildirimler = []

        for i, j in notifications:
            i.is_read = j # Dinamik olarak is_read değerini ekleme
            bildirimler.append(i)

        return bildirimler

# Kullanıcıya ait bildirimleri sil
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

# Bildirimi okundu olarak işaretleme
def is_read_notification(db: Session, notification_id: int, current_user: LoginData):
    try:
        result = db.execute(
            notification_receivers.update().where(
                and_(notification_receivers.c.notification_id == notification_id, # --> Üç koşul da sağlanıyorsa is_read güncellenecek
                notification_receivers.c.user_id == current_user.id,
                notification_receivers.c.is_removed == False)
            ).values(is_read=True)
        )

        if result.rowcount == 0:
            return {"success": False, "message": "Bildirim bulunamadı veya zaten güncellenmiş."}

        db.commit()
        return {"success": True, "message": "Bildirim okundu olarak işaretlendi.", "notification_id": notification_id,
                "is_read": True}

    except Exception as e:
        db.rollback() # --> Hata durumunda işlemi geri al
        raise HTTPException(status_code=500, detail=f"Bildirim işaretlenirken bir hata oluştu: {str(e)}")

# Belirli bir bildirimin detaylarını getirme
def notification_detail(db: Session, notification_id: int, current_user: LoginData):
    try:
        notification_entry = db.query(NotificationData, notification_receivers.c.is_read).join(
            notification_receivers,
            NotificationData.id == notification_receivers.c.notification_id
        ).filter(and_(
            notification_receivers.c.user_id == current_user.id,
            notification_receivers.c.notification_id == notification_id,
            notification_receivers.c.is_removed == False
        )).first()

        if not notification_entry:
            raise HTTPException(status_code=404, detail="Bildirimi bulunamadı.")

        notification, is_read = notification_entry

        if not is_read:
            is_read_notification(db, notification_id, current_user)

        sender = db.query(LoginData).filter(LoginData.id == notification.sender_id).first()

        return {
            "id": notification.id,
            "content": notification.content,
            "created_time": notification.created_time.isoformat(),
            "sender": {
                "id": sender.id,
                "username": sender.username
            },
            "is_read": is_read
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bildirim detayları alınırken bir hata oluştu: {str(e)}")