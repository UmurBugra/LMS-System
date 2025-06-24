from sqlalchemy.orm import Session

from crud.notification import create_notification_for_all_students
from db.models import CalendarData, LoginData
from schemas import CalendarBase, Courses, UserType, LoginBase
from fastapi import HTTPException

# CRUD operations for Calendar

def create_calendar(db: Session, request: CalendarData, current_user: LoginBase):
    username = current_user.username
    calendar_entry = CalendarData(
        days=request.day,
        t_08_09=request.t_08_09,
        t_09_10=request.t_09_10,
        t_10_11=request.t_10_11,
        t_11_12=request.t_11_12,
        t_13_14=request.t_13_14,
        t_14_15=request.t_14_15,
        t_15_16=request.t_15_16,
        t_16_17=request.t_16_17,
        user_name=current_user.username
    )
    db.add(calendar_entry)
    db.commit()
    db.refresh(calendar_entry)

    #Öğrencilere bildirim gönderme
    message = f"{username} kullanıcısı {request.day.value} günü için yeni bir takvim oluşturdu."
    create_notification_for_all_students(db, content=message, sender_username=username)

    return calendar_entry

# token fonksiyonu
def create_calendar_by_auth(db: Session, username: str, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.username == username, LoginData.type == user_type).first()
    if not user:
        raise HTTPException(status_code=404, detail="Takvim oluşturma sadece öğretmen yetkisindedir.")
    return user

# Takvim silme işlemi
def delete_calendar(db: Session, calendar_id: int, current_user: LoginBase):
    calendar_entry = db.query(CalendarData).filter(CalendarData.id == calendar_id, CalendarData.user_name == current_user.username).first()
    if not calendar_entry:
        raise HTTPException(status_code=404, detail="Takvim bulunamadı.")

    if calendar_entry.user_name != current_user.username:
        raise HTTPException(status_code=403, detail="Bu takvimi silme yetkiniz yok.")

    db.delete(calendar_entry)
    db.commit()
    return {"detail": "Takvim başarıyla silindi."}

def get_calendar(db: Session):
    calendars = db.query(CalendarData).all()
    for i in calendars:
        if i.days == CalendarBase.Pazartesi:
            i.days = "Pazartesi"
        elif i.days == CalendarBase.Salı:
            i.days = "Salı"
        elif i.days == CalendarBase.Çarşamba:
            i.days = "Çarşamba"
        elif i.days == CalendarBase.Perşembe:
            i.days = "Perşembe"
        elif i.days == CalendarBase.Cuma:
            i.days = "Cuma"
    return calendars