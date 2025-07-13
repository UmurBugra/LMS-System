from sqlalchemy.orm import Session
from crud.notification import calendar_notification_for_student
from db.models import CalendarData, LoginData
from schemas import CalendarBase, UserType, LoginBase
from fastapi import HTTPException

# CRUD operations for Calendar

# Takvim oluşturma işlemi
def create_calendar(db: Session, request: CalendarData, current_user: LoginBase):
    username = current_user
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
        user_id=current_user.id
    )
    db.add(calendar_entry)
    db.commit()
    db.refresh(calendar_entry)

    #Öğrencilere bildirim gönderme
    message = f"{username.username} kullanıcısı {request.day.value} günü için yeni bir takvim oluşturdu."
    calendar_notification_for_student(db, calendar_entry, content=message, sender_id=username.id)

    return calendar_entry

# token fonksiyonu
def create_calendar_by_auth(db: Session, email: str, user_id: int, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.email == email, LoginData.id == user_id,LoginData.type == user_type).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not a teacher")
    return user

# Takvim silme işlemi
def delete_calendar(db: Session, calendar_id: int, current_user: LoginBase):
    calendar_entry = db.query(CalendarData).filter(CalendarData.id == calendar_id, CalendarData.user_id == current_user.id).first()
    if not calendar_entry:
        raise HTTPException(status_code=404, detail="Takvim bulunamadı.")

    if calendar_entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu takvimi silme yetkiniz yok.")

    db.delete(calendar_entry)
    db.commit()
    return {"detail": "Takvim başarıyla silindi."}

# Takvim listeleme işlemi, güncellenmiş gün isimleriyle vs. kullanıcıya döndürülür.
def get_calendar(db: Session):
    calendars = db.query(CalendarData).join(LoginData, CalendarData.user_id == LoginData.id).all()
    for i in calendars:

        i.user_name = i.user.username  # --> Dinamik olarak kullanıcı adını eklemek.

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

def get_calendar_detail(db: Session, calendar_id: int):
    """Takvim detaylarını ID'ye göre getirir"""
    calendar_entry = db.query(CalendarData).filter(CalendarData.id == calendar_id).first()
    if not calendar_entry:
        raise HTTPException(status_code=404, detail="Takvim bulunamadı.")

    creator = db.query(LoginData).filter(LoginData.id == calendar_entry.user_id).first()

    # Gün adını insan dostu formata çevir
    day_name = calendar_entry.days
    if calendar_entry.days == CalendarBase.Pazartesi:
        day_name = "Pazartesi"
    elif calendar_entry.days == CalendarBase.Salı:
        day_name = "Salı"
    elif calendar_entry.days == CalendarBase.Çarşamba:
        day_name = "Çarşamba"
    elif calendar_entry.days == CalendarBase.Perşembe:
        day_name = "Perşembe"
    elif calendar_entry.days == CalendarBase.Cuma:
        day_name = "Cuma"

    return {
        "id": calendar_entry.id,
        "days": day_name,
        "t_08_09": calendar_entry.t_08_09,
        "t_09_10": calendar_entry.t_09_10,
        "t_10_11": calendar_entry.t_10_11,
        "t_11_12": calendar_entry.t_11_12,
        "t_13_14": calendar_entry.t_13_14,
        "t_14_15": calendar_entry.t_14_15,
        "t_15_16": calendar_entry.t_15_16,
        "t_16_17": calendar_entry.t_16_17,
        "creator": {
            "id": creator.id,
            "username": creator.username
        } if creator else None
    }